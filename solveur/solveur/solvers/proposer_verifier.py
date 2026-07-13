"""X-64 — ProposerVerifierSolver : le LLM propose k programmes DSL, l'interpréteur vérifie.

Un appel oracle par tâche (temp 0.0) ; si aucun programme proposé ne
reproduit TOUTES les paires train, un second appel à 0.7. Parmi les
programmes vérifiés : départage MDL (plus court, puis lexicographique) ;
les 2 meilleurs fournissent les 2 tentatives ARC. La réponse soumise est
donc toujours accompagnée d'un programme lisible et vérifié (`meta`).
"""

from __future__ import annotations

import numpy as np

from solveur.data.loader import Grid, Task
from solveur.dsl.core import Primitive, Program, run_program
from solveur.dsl.parse import dsl_reference, extract_programs, serialize_program
from solveur.oracle.client import OracleClient, OracleConfig, load_prompt
from solveur.solvers.direct_llm import CONFIG_DIR, serialize_grid

ATTEMPT_TEMPERATURES = (0.0, 0.7)
DEFAULT_K = 8  # nombre max de programmes demandés par appel (hypothèse X-64 : k ≤ 8)


def build_prompt(template: str, task: Task, k: int) -> str:
    examples = []
    for i, (grid_in, grid_out) in enumerate(task.train_pairs, 1):
        examples.append(
            f"Example {i}:\nInput:\n{serialize_grid(grid_in)}\n"
            f"Output:\n{serialize_grid(grid_out)}"
        )
    return template.format(
        train_examples="\n\n".join(examples), dsl_reference=dsl_reference(), k=k
    )


def verify_program(
    program: Program, prims: dict[str, Primitive], task: Task
) -> bool:
    """Vrai ssi le programme reproduit exactement TOUTES les paires train."""
    for grid_in, grid_out in task.train_pairs:
        out = run_program(program, prims, grid_in)
        if out is None or out.shape != grid_out.shape or not np.array_equal(out, grid_out):
            return False
    return True


class ProposerVerifierSolver:
    """Proposeur LLM + vérifieur symbolique, branché sur le runner (X-52)."""

    def __init__(
        self,
        config_path: str | None = None,
        use_cache: bool = True,
        k: int = DEFAULT_K,
        name: str = "pv-haiku",
    ) -> None:
        self._config_path = config_path or str(CONFIG_DIR / "propose_haiku.yaml")
        self._use_cache = use_cache
        self.k = k
        self.name = name
        self.meta: dict[str, object] = {}
        self.budget_usd_per_run = OracleConfig.from_yaml(self._config_path).budget_usd_per_run
        self._client: OracleClient | None = None
        self.prompt = load_prompt("propose_v1")

    def _oracle(self) -> OracleClient:
        # Paresseux : le runner fork chaque solve, SQLite s'ouvre côté enfant.
        if self._client is None:
            config = OracleConfig.from_yaml(self._config_path)
            self._client = OracleClient(config, use_cache=self._use_cache)
        return self._client

    def solve(self, task: Task) -> list[list[Grid]]:
        oracle = self._oracle()
        prompt = build_prompt(self.prompt["template"], task, self.k)
        cost = 0.0
        proposed: list[str] = []
        rejected: list[tuple[str, str]] = []
        verified: list[tuple[Program, dict[str, Primitive]]] = []
        seen: set[Program] = set()
        for temperature in ATTEMPT_TEMPERATURES:
            response = oracle.complete(
                prompt,
                task_id=task.task_id,
                temperature=temperature,
                prompt_ref=f"{self.prompt['id']}_{self.prompt['version']}",
            )
            cost += response.cost_usd
            extraction = extract_programs(response.text, k=self.k)
            rejected.extend(extraction.rejected)
            for program, prims in extraction.programs:
                if program in seen:
                    continue
                seen.add(program)
                proposed.append(serialize_program(program))
                if verify_program(program, prims, task):
                    verified.append((program, prims))
                else:
                    rejected.append((serialize_program(program), "ne reproduit pas le train"))
            if verified:
                break  # pas de second appel si le premier suffit

        # départage MDL : plus court, puis lexicographique ; top-2 = 2 tentatives ARC
        verified.sort(key=lambda pv: (len(pv[0]), pv[0]))
        best = verified[:2]
        attempts: list[list[Grid]] = []
        for test_in, _expected in task.test_pairs:
            tries: list[Grid] = []
            for program, prims in best:
                out = run_program(program, prims, test_in)
                if out is not None:
                    tries.append(out)
            attempts.append(tries)

        self.meta = {
            "cost_usd": cost,
            "prompt_sha256": self.prompt["sha256"],
            "prompt_ref": f"{self.prompt['id']}_{self.prompt['version']}",
            "k": self.k,
            "proposed": proposed,
            "rejected": [{"program": p, "reason": r} for p, r in rejected],
            "verified": [serialize_program(p) for p, _ in verified],
            "program": serialize_program(best[0][0]) if best else None,
        }
        if not proposed and rejected:
            self.meta["status"] = "parse_error"
        return attempts
