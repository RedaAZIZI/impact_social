"""Runner d'évaluation (X-52).

- Interface `Solver` : solve(task) -> list[list[Grid]] — attempts[i] contient
  jusqu'à 2 tentatives pour task.test_pairs[i] (règle officielle ARC).
- Sandbox : chaque solve tourne dans un sous-processus (fork) avec timeout
  configurable (défaut 60 s) et limite mémoire (défaut 2 Go, RLIMIT_AS).
  Timeout ou crash = tâche non résolue, jamais un crash du runner.
- Scoring officiel : tâche résolue si, pour CHAQUE test, une des tentatives
  correspond exactement à la sortie attendue (toutes les cellules).
- Tracking : runs.db (SQLite) — run + statut par tâche.
"""

from __future__ import annotations

import json
import multiprocessing
import resource
import sqlite3
import subprocess
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

import numpy as np

from solveur.data.loader import Grid, Task

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = PROJECT_ROOT / "runs.db"

DEFAULT_TIMEOUT_S = 60.0
DEFAULT_MEMORY_BYTES = 2 * 1024**3


class Solver(Protocol):
    """Un solveur ARC. attempts[i] = jusqu'à 2 tentatives pour test_pairs[i].

    L'attribut optionnel `meta` (dict) est relevé après solve() et journalisé
    (ex. cost_usd, parse_errors).
    """

    name: str

    def solve(self, task: Task) -> list[list[Grid]]: ...


@dataclass
class TaskResult:
    task_id: str
    status: str  # solved | failed | timeout | crash | parse_error
    duration_s: float
    cost_usd: float = 0.0
    n_attempts: int = 0
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvalRun:
    run_id: str
    solver_name: str
    git_sha: str
    split: str
    score: float
    n_tasks: int
    n_solved: int
    cost_usd: float
    duration_s: float
    results: list[TaskResult]


def grids_equal(a: Grid, b: Grid) -> bool:
    return a.shape == b.shape and bool(np.array_equal(a, b))


def _git_sha() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, timeout=10
        )
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def _child_solve(solver: Solver, task: Task, memory_bytes: int, conn: Any) -> None:
    try:
        resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
        attempts = solver.solve(task)
        payload = [[np.asarray(g, dtype=np.int8) for g in per_test] for per_test in attempts]
        conn.send(("ok", payload, dict(getattr(solver, "meta", {}) or {})))
    except BaseException:
        try:
            conn.send(("error", traceback.format_exc(limit=5), {}))
        except Exception:
            pass
    finally:
        conn.close()


def _sandboxed_solve(
    solver: Solver, task: Task, timeout_s: float, memory_bytes: int
) -> tuple[str, Any, dict[str, Any]]:
    """Exécute solve() dans un sous-processus. Retourne (status, attempts, meta)."""
    ctx = multiprocessing.get_context("fork")
    parent_conn, child_conn = ctx.Pipe(duplex=False)
    proc = ctx.Process(target=_child_solve, args=(solver, task, memory_bytes, child_conn))
    proc.start()
    child_conn.close()
    try:
        if parent_conn.poll(timeout_s):
            kind, payload, meta = parent_conn.recv()
        else:
            proc.kill()
            return "timeout", None, {}
    except EOFError:  # le process est mort sans rien envoyer (segfault, OOM)
        return "crash", None, {}
    finally:
        proc.join(timeout=5)
        if proc.is_alive():
            proc.kill()
            proc.join()
        parent_conn.close()
    if kind == "error":
        return "crash", None, {"traceback": payload}
    return "ok", payload, meta


def score_attempts(task: Task, attempts: list[list[Grid]]) -> bool:
    """Officiel : résolu si chaque test a une tentative (≤2) exactement correcte."""
    if len(attempts) < len(task.test_pairs):
        return False
    for (_test_in, expected), tries in zip(task.test_pairs, attempts, strict=False):
        if not any(grids_equal(t, expected) for t in tries[:2]):
            return False
    return True


def _init_db(db: sqlite3.Connection) -> None:
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY, solver_name TEXT, git_sha TEXT, split TEXT,
            started_at REAL, score REAL, n_tasks INTEGER, n_solved INTEGER,
            cost_usd REAL, duration_s REAL
        );
        CREATE TABLE IF NOT EXISTS task_results (
            run_id TEXT, task_id TEXT, status TEXT, duration_s REAL,
            cost_usd REAL, n_attempts INTEGER, meta_json TEXT,
            PRIMARY KEY (run_id, task_id)
        );
        """
    )
    db.commit()


def run_eval(
    solver: Solver,
    tasks: list[Task],
    split: str,
    run_id: str | None = None,
    db_path: Path | str | None = None,
    timeout_s: float = DEFAULT_TIMEOUT_S,
    memory_bytes: int = DEFAULT_MEMORY_BYTES,
    verbose: bool = False,
) -> EvalRun:
    started_at = time.time()
    run_id = run_id or f"{solver.name}-{int(started_at)}"
    results: list[TaskResult] = []

    for task in tasks:
        t0 = time.time()
        status, attempts, meta = _sandboxed_solve(solver, task, timeout_s, memory_bytes)
        if status == "ok":
            solved = score_attempts(task, attempts)
            status = "solved" if solved else str(meta.get("status", "failed"))
        n_attempts = sum(len(per_test) for per_test in attempts) if attempts else 0
        extra_meta = {k: v for k, v in meta.items() if k not in ("cost_usd",)}
        if attempts is not None:
            # grilles produites, persistées pour le rapport X-56 (viz + taxonomie)
            extra_meta["attempts"] = [
                [np.asarray(g).tolist() for g in per_test] for per_test in attempts
            ]
        results.append(
            TaskResult(
                task_id=task.task_id,
                status=status,
                duration_s=time.time() - t0,
                cost_usd=float(meta.get("cost_usd", 0.0)),
                n_attempts=n_attempts,
                meta=extra_meta,
            )
        )
        if verbose:
            print(f"  {task.task_id}: {status} ({results[-1].duration_s:.1f}s)")

    n_solved = sum(1 for r in results if r.status == "solved")
    run = EvalRun(
        run_id=run_id,
        solver_name=solver.name,
        git_sha=_git_sha(),
        split=split,
        score=n_solved / len(results) if results else 0.0,
        n_tasks=len(results),
        n_solved=n_solved,
        cost_usd=sum(r.cost_usd for r in results),
        duration_s=time.time() - started_at,
        results=results,
    )

    db = sqlite3.connect(str(db_path or DEFAULT_DB_PATH))
    _init_db(db)
    db.execute(
        "INSERT OR REPLACE INTO runs VALUES (?,?,?,?,?,?,?,?,?,?)",
        (
            run.run_id, run.solver_name, run.git_sha, run.split, started_at,
            run.score, run.n_tasks, run.n_solved, run.cost_usd, run.duration_s,
        ),
    )
    db.executemany(
        "INSERT OR REPLACE INTO task_results VALUES (?,?,?,?,?,?,?)",
        [
            (
                run.run_id, r.task_id, r.status, r.duration_s,
                r.cost_usd, r.n_attempts, json.dumps(r.meta, default=str),
            )
            for r in run.results
        ],
    )
    db.commit()
    db.close()
    return run
