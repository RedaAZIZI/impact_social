"""X-52 — critères d'acceptation du runner sandboxé."""

from __future__ import annotations

import ctypes
import sqlite3
import time
from pathlib import Path

import numpy as np
import pytest

from solveur.data.loader import Grid, Task
from solveur.eval.runner import run_eval
from solveur.solvers import RandomSolver


def make_task(i: int) -> Task:
    grid_in = np.full((3, 3), i % 10, dtype=np.int8)
    grid_out = np.rot90(grid_in).copy()
    return Task(
        task_id=f"mock/{i}",
        source="mock",
        train_pairs=[(grid_in, grid_out)],
        test_pairs=[(grid_in, grid_out)],
    )


TASKS = [make_task(i) for i in range(4)]


class PerfectSolver:
    name = "perfect"

    def solve(self, task: Task) -> list[list[Grid]]:
        return [[expected] for _test_in, expected in task.test_pairs]


class InfiniteSolver:
    name = "infinite"

    def solve(self, task: Task) -> list[list[Grid]]:
        while True:
            time.sleep(0.1)


class RaisingSolver:
    name = "raising"

    def solve(self, task: Task) -> list[list[Grid]]:
        raise ValueError("boom")


class SegfaultSolver:
    name = "segfault"

    def solve(self, task: Task) -> list[list[Grid]]:
        ctypes.string_at(0)  # déréférence NULL → SIGSEGV
        return []


def test_perfect_solver(tmp_path: Path) -> None:
    run = run_eval(PerfectSolver(), TASKS, split="mock", db_path=tmp_path / "runs.db")
    assert run.score == 1.0
    assert all(r.status == "solved" for r in run.results)


def test_random_solver(tmp_path: Path) -> None:
    run = run_eval(RandomSolver(), TASKS, split="mock", db_path=tmp_path / "runs.db")
    assert run.score <= 0.25  # ~0%, aucune exception levée
    assert run.n_tasks == len(TASKS)


def test_timeout_isolation(tmp_path: Path) -> None:
    run = run_eval(
        InfiniteSolver(), TASKS[:2], split="mock", db_path=tmp_path / "runs.db", timeout_s=1.0
    )
    assert [r.status for r in run.results] == ["timeout", "timeout"]  # le run continue


def test_crash_isolation(tmp_path: Path) -> None:
    for solver in (RaisingSolver(), SegfaultSolver()):
        run = run_eval(solver, TASKS[:2], split="mock", db_path=tmp_path / "runs.db")
        assert all(r.status == "crash" for r in run.results)
        assert run.n_tasks == 2  # le runner n'a pas crashé


def test_run_recorded(tmp_path: Path) -> None:
    db_path = tmp_path / "runs.db"
    run = run_eval(PerfectSolver(), TASKS, split="mock", run_id="test-run", db_path=db_path)
    db = sqlite3.connect(db_path)
    row = db.execute(
        "SELECT run_id, solver_name, git_sha, split, score, cost_usd FROM runs"
    ).fetchone()
    assert row[0] == "test-run" and row[1] == "perfect" and row[3] == "mock"
    assert row[2] == run.git_sha and len(row[2]) >= 7  # git_sha présent
    assert row[5] == pytest.approx(0.0)  # coût
    n = db.execute("SELECT COUNT(*) FROM task_results WHERE run_id='test-run'").fetchone()[0]
    assert n == len(TASKS)


# --- X-61 : infra runs — reprise, plafond global, timeout journalisé ---


class TracingSolver:
    """Solveur déterministe qui écrit une trace par tâche résolue.

    La trace (un fichier par task_id) survit au fork du sandbox : elle
    prouve quelles tâches ont réellement appelé le solveur (≙ l'oracle).
    """

    name = "tracing"

    def __init__(self, trace_dir: Path, cost_per_task: float = 0.0) -> None:
        self.trace_dir = trace_dir
        self.meta = {"cost_usd": cost_per_task}

    def solve(self, task: Task) -> list[list[Grid]]:
        (self.trace_dir / task.task_id.replace("/", "_")).touch()
        return [[expected] for _test_in, expected in task.test_pairs]


def _dump_deterministic(db_path: Path) -> tuple[list, list]:
    """Contenu de runs.db sans les champs horodatés (durées, started_at)."""
    db = sqlite3.connect(db_path)
    runs = db.execute(
        "SELECT run_id, solver_name, git_sha, split, score, n_tasks, n_solved,"
        " cost_usd, status, n_done, timeout_s FROM runs ORDER BY run_id"
    ).fetchall()
    task_results = db.execute(
        "SELECT run_id, task_id, status, cost_usd, n_attempts, meta_json"
        " FROM task_results ORDER BY run_id, task_id"
    ).fetchall()
    db.close()
    return runs, task_results


def test_resume_identical_to_uninterrupted(tmp_path: Path) -> None:
    """Critère X-61 : kill simulé + --resume ⇒ même contenu de runs.db qu'un
    run ininterrompu, sans réappeler l'oracle pour les tâches déjà faites."""
    # run ininterrompu (référence)
    ref_db = tmp_path / "ref.db"
    ref_traces = tmp_path / "ref_traces"
    ref_traces.mkdir()
    run_eval(TracingSolver(ref_traces), TASKS, split="mock", run_id="r", db_path=ref_db)

    # run interrompu après 2 tâches (kill simulé), puis repris
    db_path = tmp_path / "runs.db"
    traces = tmp_path / "traces"
    traces.mkdir()
    run_eval(TracingSolver(traces), TASKS[:2], split="mock", run_id="r", db_path=db_path)
    db = sqlite3.connect(db_path)
    n_before, status_before = db.execute(
        "SELECT (SELECT COUNT(*) FROM task_results), status FROM runs"
    ).fetchone()
    db.close()
    assert n_before == 2  # les résultats partiels sont déjà persistés
    assert {p.name for p in traces.iterdir()} == {"mock_0", "mock_1"}

    resumed = run_eval(
        TracingSolver(traces), TASKS, split="mock", run_id="r", db_path=db_path, resume=True
    )
    # les 2 tâches déjà faites n'ont PAS réappelé le solveur/oracle
    assert {p.name for p in traces.iterdir()} == {f"mock_{i}" for i in range(4)}
    assert [r.task_id for r in resumed.results] == ["mock/2", "mock/3"]
    assert resumed.status == "complete" and resumed.n_done == 4

    assert _dump_deterministic(db_path) == _dump_deterministic(ref_db)


def test_resume_skips_all_when_complete(tmp_path: Path) -> None:
    db_path = tmp_path / "runs.db"
    traces = tmp_path / "traces"
    traces.mkdir()
    run_eval(TracingSolver(traces), TASKS, split="mock", run_id="r", db_path=db_path)
    before = _dump_deterministic(db_path)
    resumed = run_eval(
        TracingSolver(traces), TASKS, split="mock", run_id="r", db_path=db_path, resume=True
    )
    assert resumed.results == []  # aucun réappel
    assert _dump_deterministic(db_path) == before


def test_budget_per_run_clean_stop(tmp_path: Path) -> None:
    """Critère X-61 : plafond global ⇒ arrêt propre, run partiel journalisé."""
    db_path = tmp_path / "runs.db"
    traces = tmp_path / "traces"
    traces.mkdir()
    solver = TracingSolver(traces, cost_per_task=0.6)
    run = run_eval(
        solver, TASKS, split="mock", run_id="r", db_path=db_path, budget_usd_per_run=1.0
    )
    # 0.6 après la 1re tâche (< 1.0), 1.2 après la 2e (>= 1.0) → arrêt avant la 3e
    assert run.status == "budget_stop"
    assert run.n_done == 2 and run.n_tasks == 4
    assert run.cost_usd == pytest.approx(1.2)
    db = sqlite3.connect(db_path)
    row = db.execute(
        "SELECT status, n_done, n_tasks, score, cost_usd FROM runs WHERE run_id='r'"
    ).fetchone()
    n_results = db.execute("SELECT COUNT(*) FROM task_results WHERE run_id='r'").fetchone()[0]
    db.close()
    assert row == ("budget_stop", 2, 4, pytest.approx(0.5), pytest.approx(1.2))
    assert n_results == 2  # le partiel est bien écrit


def test_budget_counts_resumed_cost(tmp_path: Path) -> None:
    """La reprise hérite du coût déjà dépensé : plafond déjà atteint ⇒ stop immédiat."""
    db_path = tmp_path / "runs.db"
    traces = tmp_path / "traces"
    traces.mkdir()
    solver = TracingSolver(traces, cost_per_task=0.6)
    run_eval(solver, TASKS[:2], split="mock", run_id="r", db_path=db_path)
    resumed = run_eval(
        solver, TASKS, split="mock", run_id="r", db_path=db_path,
        resume=True, budget_usd_per_run=1.0,
    )
    assert resumed.status == "budget_stop" and resumed.results == []
    assert resumed.n_done == 2


def test_default_timeout_and_journal(tmp_path: Path) -> None:
    """X-61 : timeout par défaut 120 s, journalisé dans runs pour mesure d'impact."""
    from solveur.eval.runner import DEFAULT_TIMEOUT_S

    assert DEFAULT_TIMEOUT_S == 120.0
    db_path = tmp_path / "runs.db"
    run_eval(PerfectSolver(), TASKS[:1], split="mock", run_id="r", db_path=db_path)
    db = sqlite3.connect(db_path)
    timeout_s = db.execute("SELECT timeout_s FROM runs WHERE run_id='r'").fetchone()[0]
    duration = db.execute("SELECT duration_s FROM task_results").fetchone()[0]
    db.close()
    assert timeout_s == 120.0
    assert duration > 0.0  # temps utilisé journalisé par tâche


def test_migration_legacy_db(tmp_path: Path) -> None:
    """Un runs.db d'avant X-61 (schéma EPIC-0) reste lisible et migrable."""
    db_path = tmp_path / "runs.db"
    db = sqlite3.connect(db_path)
    db.executescript(
        """
        CREATE TABLE runs (
            run_id TEXT PRIMARY KEY, solver_name TEXT, git_sha TEXT, split TEXT,
            started_at REAL, score REAL, n_tasks INTEGER, n_solved INTEGER,
            cost_usd REAL, duration_s REAL
        );
        CREATE TABLE task_results (
            run_id TEXT, task_id TEXT, status TEXT, duration_s REAL,
            cost_usd REAL, n_attempts INTEGER, meta_json TEXT,
            PRIMARY KEY (run_id, task_id)
        );
        INSERT INTO runs VALUES ('legacy', 's', 'sha', 'dev', 0, 0.5, 2, 1, 1.0, 10.0);
        """
    )
    db.commit()
    db.close()
    run_eval(PerfectSolver(), TASKS[:1], split="mock", run_id="new", db_path=db_path)
    db = sqlite3.connect(db_path)
    legacy = db.execute("SELECT status FROM runs WHERE run_id='legacy'").fetchone()[0]
    db.close()
    assert legacy == "complete"  # les runs gelés EPIC-0 restent marqués complets
