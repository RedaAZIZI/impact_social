"""X-54 — Baseline 1 : LLM en prompting direct, prompt gelé direct_v1.

2 tentatives par test : température 0.0 puis 0.7. Sortie imparsable =
tentative échouée, catégorie parse_error. Le solveur journalise dans `meta`
le coût, le taux de parse_error et le sha256 du prompt (gel vérifiable).
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np

from solveur.data.loader import Grid, Task
from solveur.oracle.client import OracleClient, OracleConfig, load_prompt

CONFIG_DIR = Path(__file__).resolve().parents[2] / "configs"

ATTEMPT_TEMPERATURES = (0.0, 0.7)

_OUTPUT_RE = re.compile(r"<output>\s*(.*?)\s*</output>", re.DOTALL)


def serialize_grid(grid: Grid) -> str:
    return "\n".join(" ".join(str(int(v)) for v in row) for row in grid)


def build_prompt(template: str, task: Task, test_in: Grid) -> str:
    examples = []
    for i, (grid_in, grid_out) in enumerate(task.train_pairs, 1):
        examples.append(
            f"Example {i}:\nInput:\n{serialize_grid(grid_in)}\n"
            f"Output:\n{serialize_grid(grid_out)}"
        )
    return template.format(
        train_examples="\n\n".join(examples), test_input=serialize_grid(test_in)
    )


def parse_grid(text: str) -> Grid | None:
    """Extrait la dernière grille du bloc <output>. None si imparsable."""
    matches = _OUTPUT_RE.findall(text)
    if not matches:
        return None
    rows = []
    for line in matches[-1].strip().splitlines():
        line = line.strip()
        if not line:
            continue
        cells = line.split() if " " in line else list(line)
        try:
            row = [int(c) for c in cells]
        except ValueError:
            return None
        if not all(0 <= v <= 9 for v in row):
            return None
        rows.append(row)
    if not rows or len({len(r) for r in rows}) != 1:
        return None
    if len(rows) > 30 or len(rows[0]) > 30:
        return None
    return np.array(rows, dtype=np.int8)


class DirectLLMSolver:
    """Baseline LLM direct, branchée sur le runner via l'oracle (X-53)."""

    def __init__(self, config_path: Path | str, use_cache: bool = True, name: str | None = None):
        self._config_path = Path(config_path)
        self._use_cache = use_cache
        self.name = name or f"direct-{self._config_path.stem.split('_')[-1]}"
        self.meta: dict[str, object] = {}
        # plafond global du run, relevé par le runner (X-61)
        self.budget_usd_per_run = OracleConfig.from_yaml(self._config_path).budget_usd_per_run
        self._client: OracleClient | None = None
        self.prompt = load_prompt("direct_v1")

    def _oracle(self) -> OracleClient:
        # Créé paresseusement : le runner fork chaque solve dans un sous-processus,
        # les connexions SQLite doivent être ouvertes côté enfant.
        if self._client is None:
            config = OracleConfig.from_yaml(self._config_path)
            self._client = OracleClient(config, use_cache=self._use_cache)
        return self._client

    def solve(self, task: Task) -> list[list[Grid]]:
        oracle = self._oracle()
        attempts: list[list[Grid]] = []
        parse_errors = 0
        cost = 0.0
        for test_in, _expected in task.test_pairs:
            prompt = build_prompt(self.prompt["template"], task, test_in)
            tries: list[Grid] = []
            for temperature in ATTEMPT_TEMPERATURES:
                response = oracle.complete(
                    prompt,
                    task_id=task.task_id,
                    temperature=temperature,
                    prompt_ref=f"{self.prompt['id']}_{self.prompt['version']}",
                )
                cost += response.cost_usd
                grid = parse_grid(response.text)
                if grid is None:
                    parse_errors += 1
                else:
                    tries.append(grid)
            attempts.append(tries)
        n_attempts = 2 * len(task.test_pairs)
        self.meta = {
            "cost_usd": cost,
            "parse_errors": parse_errors,
            "parse_error_rate": parse_errors / n_attempts if n_attempts else 0.0,
            "prompt_sha256": self.prompt["sha256"],
            "prompt_ref": f"{self.prompt['id']}_{self.prompt['version']}",
        }
        if parse_errors == n_attempts:
            self.meta["status"] = "parse_error"
        return attempts
