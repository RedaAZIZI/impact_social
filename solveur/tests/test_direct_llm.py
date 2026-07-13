"""X-54 — tests du DirectLLMSolver (mocks, zéro appel réseau)."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

from solveur.data.loader import Task
from solveur.eval.runner import run_eval
from solveur.oracle.client import load_prompt
from solveur.solvers.direct_llm import (
    CONFIG_DIR,
    DirectLLMSolver,
    build_prompt,
    parse_grid,
    serialize_grid,
)

G = lambda rows: np.array(rows, dtype=np.int8)  # noqa: E731

TASK = Task(
    task_id="mock/llm",
    source="mock",
    train_pairs=[(G([[1, 2], [3, 4]]), G([[4, 3], [2, 1]]))],
    test_pairs=[(G([[5, 6], [7, 8]]), G([[8, 7], [6, 5]]))],
)


class TestParsing:
    def test_parse_valid(self) -> None:
        grid = parse_grid("blabla raisonnement\n<output>\n8 7\n6 5\n</output>")
        assert np.array_equal(grid, G([[8, 7], [6, 5]]))

    def test_parse_compact_digits(self) -> None:
        grid = parse_grid("<output>\n87\n65\n</output>")
        assert np.array_equal(grid, G([[8, 7], [6, 5]]))

    def test_parse_takes_last_block(self) -> None:
        text = "<output>\n1\n</output> non, plutôt : <output>\n2\n</output>"
        assert np.array_equal(parse_grid(text), G([[2]]))

    def test_parse_errors(self) -> None:
        assert parse_grid("pas de bloc du tout") is None
        assert parse_grid("<output>\n1 2\n3\n</output>") is None  # non rectangulaire
        assert parse_grid("<output>\na b\n</output>") is None  # non numérique
        assert parse_grid("<output>\n</output>") is None  # vide


def test_serialize_roundtrip() -> None:
    grid = G([[0, 5, 9], [1, 2, 3]])
    assert np.array_equal(parse_grid(f"<output>\n{serialize_grid(grid)}\n</output>"), grid)


def make_solver(tmp_path: Path, response_text: str, config: str = "direct_haiku"):  # type: ignore[no-untyped-def]
    import io

    from solveur.oracle.client import OracleClient, OracleConfig

    solver = DirectLLMSolver(CONFIG_DIR / f"{config}.yaml")
    transport_calls: list[dict] = []

    def transport(request: dict) -> dict:
        transport_calls.append(request)
        return {"text": response_text, "input_tokens": 100, "output_tokens": 50}

    solver._client = OracleClient(
        OracleConfig.from_yaml(CONFIG_DIR / f"{config}.yaml"),
        transport=transport,
        cache_path=tmp_path / "cache.db",
        log_stream=io.StringIO(),
    )
    return solver, transport_calls


def test_solver_solves_with_mock(tmp_path: Path) -> None:
    solver, calls = make_solver(tmp_path, "raisonnement…\n<output>\n8 7\n6 5\n</output>")
    attempts = solver.solve(TASK)
    assert np.array_equal(attempts[0][0], TASK.test_pairs[0][1])
    assert [c["temperature"] for c in calls] == [0.0, 0.7]  # 2 tentatives, temp 0 puis 0.7
    assert solver.meta["parse_errors"] == 0
    assert solver.meta["cost_usd"] > 0


def test_solver_parse_error(tmp_path: Path) -> None:
    solver, _ = make_solver(tmp_path, "je ne sais pas")
    attempts = solver.solve(TASK)
    assert attempts == [[]]
    assert solver.meta["parse_errors"] == 2
    assert solver.meta["status"] == "parse_error"


def test_parse_error_recorded_in_db(tmp_path: Path) -> None:
    solver, _ = make_solver(tmp_path, "sortie imparsable")
    run = run_eval(solver, [TASK], split="mock", db_path=tmp_path / "runs.db")
    assert run.results[0].status == "parse_error"


def test_prompt_frozen(tmp_path: Path) -> None:
    """Le hash du prompt est identique entre les runs Haiku et Sonnet."""
    haiku = DirectLLMSolver(CONFIG_DIR / "direct_haiku.yaml")
    sonnet = DirectLLMSolver(CONFIG_DIR / "direct_sonnet.yaml")
    assert haiku.prompt["sha256"] == sonnet.prompt["sha256"]
    template = load_prompt("direct_v1")["template"]
    assert haiku.prompt["sha256"] == hashlib.sha256(template.encode()).hexdigest()

    prompt_h = build_prompt(haiku.prompt["template"], TASK, TASK.test_pairs[0][0])
    prompt_s = build_prompt(sonnet.prompt["template"], TASK, TASK.test_pairs[0][0])
    assert prompt_h == prompt_s  # prompt final strictement identique
