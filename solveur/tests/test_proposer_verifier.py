"""X-64 — tests du ProposerVerifierSolver (mocks, zéro appel réseau)."""

from __future__ import annotations

import io
from pathlib import Path

import numpy as np

from solveur.data.loader import Task
from solveur.dsl.core import PRIMITIVE_FACTORIES
from solveur.eval.runner import run_eval
from solveur.oracle.client import OracleClient, OracleConfig
from solveur.solvers import build_solver, list_solvers
from solveur.solvers.direct_llm import CONFIG_DIR
from solveur.solvers.proposer_verifier import (
    ProposerVerifierSolver,
    build_prompt,
    verify_program,
)

G = lambda rows: np.array(rows, dtype=np.int8)  # noqa: E731

# transformation : rotation de 180°
TASK = Task(
    task_id="mock/pv",
    source="mock",
    train_pairs=[
        (G([[1, 2], [3, 4]]), G([[4, 3], [2, 1]])),
        (G([[5, 0], [0, 0]]), G([[0, 0], [0, 5]])),
    ],
    test_pairs=[(G([[5, 6], [7, 8]]), G([[8, 7], [6, 5]]))],
)


_COUNTER = iter(range(10**6))


def make_solver(tmp_path: Path, responses: list[str]):  # type: ignore[no-untyped-def]
    solver = ProposerVerifierSolver(k=4)
    calls: list[dict] = []
    cache_path = tmp_path / f"cache_{next(_COUNTER)}.db"

    def transport(request: dict) -> dict:
        calls.append(request)
        text = responses[min(len(calls) - 1, len(responses) - 1)]
        return {"text": text, "input_tokens": 200, "output_tokens": 50}

    solver._client = OracleClient(
        OracleConfig.from_yaml(CONFIG_DIR / "propose_haiku.yaml"),
        transport=transport,
        cache_path=cache_path,
        log_stream=io.StringIO(),
    )
    return solver, calls


def test_valid_program_accepted(tmp_path: Path) -> None:
    answer = "Une rotation.\n```dsl\nrotate180\nflip_h\n```"
    solver, calls = make_solver(tmp_path, [answer])
    attempts = solver.solve(TASK)
    # rotate180 vérifie le train ; flip_h non (rejeté avec raison)
    assert solver.meta["program"] == "rotate180"
    assert np.array_equal(attempts[0][0], TASK.test_pairs[0][1])
    assert {r["program"] for r in solver.meta["rejected"]} == {"flip_h"}  # type: ignore[index]
    assert len(calls) == 1  # pas de second appel : le premier a suffi
    assert solver.meta["cost_usd"] > 0


def test_unverified_programs_trigger_retry_then_fail(tmp_path: Path) -> None:
    solver, calls = make_solver(tmp_path, ["```dsl\nflip_h\n```", "```dsl\nflip_v\n```"])
    attempts = solver.solve(TASK)
    assert attempts == [[]]
    assert solver.meta["program"] is None
    assert [c["temperature"] for c in calls] == [0.0, 0.7]


def test_mdl_tie_break_shortest_program_first(tmp_path: Path) -> None:
    answer = "```dsl\nrotate90 | rotate90\nrotate180\n```"
    solver, _ = make_solver(tmp_path, [answer])
    solver.solve(TASK)
    # les deux vérifient le train ; MDL retient le plus court
    assert solver.meta["program"] == "rotate180"
    assert solver.meta["verified"] == ["rotate180", "rotate90 | rotate90"]


def test_noisy_answer_and_parse_error_status(tmp_path: Path) -> None:
    noisy = "Je propose :\n```dsl\nfrobnicate(3)\nrotate180\nfill_enclosed(12)\n```"
    solver, _ = make_solver(tmp_path, [noisy])
    attempts = solver.solve(TASK)
    assert np.array_equal(attempts[0][0], TASK.test_pairs[0][1])  # le valide survit au bruit

    solver, _ = make_solver(tmp_path, ["aucun bloc"])
    solver.solve(TASK)
    assert solver.meta["program"] is None

    solver, _ = make_solver(tmp_path, ["```dsl\nfrobnicate(1)\n```"])
    solver.solve(TASK)
    assert solver.meta["status"] == "parse_error"


def test_runner_integration(tmp_path: Path) -> None:
    solver, _ = make_solver(tmp_path, ["```dsl\nrotate180\n```"])
    run = run_eval(solver, [TASK], split="mock", db_path=tmp_path / "runs.db")
    assert run.results[0].status == "solved"


def test_prompt_mentions_dsl_and_k() -> None:
    solver = ProposerVerifierSolver(k=4)
    prompt = build_prompt(solver.prompt["template"], TASK, solver.k)
    assert "up to 4 candidate DSL programs" in prompt
    for name in PRIMITIVE_FACTORIES:
        assert name in prompt  # la référence DSL générée couvre tout l'interpréteur


def test_verify_program_requires_all_train_pairs() -> None:
    from solveur.dsl.parse import parse_program

    program, prims = parse_program("flip_h")
    assert not verify_program(program, prims, TASK)
    program, prims = parse_program("rotate180")
    assert verify_program(program, prims, TASK)


def test_registered_in_eval_registry() -> None:
    assert "pv-haiku" in list_solvers()
    solver = build_solver("pv-haiku")
    assert solver.name == "pv-haiku"
    assert solver.budget_usd_per_run == 3.0
