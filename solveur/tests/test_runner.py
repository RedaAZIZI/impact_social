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
