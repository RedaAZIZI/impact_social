"""Runner d'évaluation (X-52, infra runs X-61).

- Interface `Solver` : solve(task) -> list[list[Grid]] — attempts[i] contient
  jusqu'à 2 tentatives pour task.test_pairs[i] (règle officielle ARC).
- Sandbox : chaque solve tourne dans un sous-processus (fork) avec timeout
  configurable (défaut 120 s) et limite mémoire (défaut 2 Go, RLIMIT_AS).
  Timeout ou crash = tâche non résolue, jamais un crash du runner.
- Scoring officiel : tâche résolue si, pour CHAQUE test, une des tentatives
  correspond exactement à la sortie attendue (toutes les cellules).
- Tracking : runs.db (SQLite) — run + statut par tâche, écrits au fil de
  l'eau : un kill du conteneur ne perd que la tâche en cours (X-61).
- Reprise : resume=True saute les tâches déjà présentes pour ce run_id
  (aucun réappel de l'oracle) et complète le run.
- Plafond global : budget_usd_per_run — arrêt propre au plafond, le run
  partiel (status=budget_stop, n_done/n_tasks) reste journalisé.
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

DEFAULT_TIMEOUT_S = 120.0
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
    n_tasks: int  # tâches planifiées (total du split), pas seulement exécutées
    n_solved: int
    cost_usd: float
    duration_s: float
    results: list[TaskResult]  # tâches exécutées par CET appel (hors reprises)
    status: str = "complete"  # complete | partial | budget_stop
    n_done: int = 0  # tâches présentes dans runs.db pour ce run (reprises incluses)


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
    # Migration X-61 : colonnes ajoutées après le gel EPIC-0 (les anciennes
    # lignes reçoivent status='complete', n_done/timeout_s NULL).
    cols = {row[1] for row in db.execute("PRAGMA table_info(runs)")}
    if "status" not in cols:
        db.execute("ALTER TABLE runs ADD COLUMN status TEXT DEFAULT 'complete'")
    if "n_done" not in cols:
        db.execute("ALTER TABLE runs ADD COLUMN n_done INTEGER")
    if "timeout_s" not in cols:
        db.execute("ALTER TABLE runs ADD COLUMN timeout_s REAL")
    db.commit()


def _write_task_result(db: sqlite3.Connection, run_id: str, r: TaskResult) -> None:
    db.execute(
        "INSERT OR REPLACE INTO task_results VALUES (?,?,?,?,?,?,?)",
        (
            run_id, r.task_id, r.status, r.duration_s,
            r.cost_usd, r.n_attempts, json.dumps(r.meta, default=str),
        ),
    )
    db.commit()


def _run_aggregates(db: sqlite3.Connection, run_id: str) -> tuple[int, int, float]:
    """(n_done, n_solved, cost_usd) recalculés depuis task_results — la reprise
    hérite ainsi exactement des tâches déjà journalisées."""
    row = db.execute(
        "SELECT COUNT(*), COALESCE(SUM(status='solved'), 0), COALESCE(SUM(cost_usd), 0.0)"
        " FROM task_results WHERE run_id=?",
        (run_id,),
    ).fetchone()
    return int(row[0]), int(row[1]), float(row[2])


def _write_run_row(
    db: sqlite3.Connection, run: EvalRun, started_at: float, timeout_s: float
) -> None:
    db.execute(
        "INSERT OR REPLACE INTO runs"
        " (run_id, solver_name, git_sha, split, started_at, score, n_tasks,"
        "  n_solved, cost_usd, duration_s, status, n_done, timeout_s)"
        " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            run.run_id, run.solver_name, run.git_sha, run.split, started_at,
            run.score, run.n_tasks, run.n_solved, run.cost_usd, run.duration_s,
            run.status, run.n_done, timeout_s,
        ),
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
    resume: bool = False,
    budget_usd_per_run: float | None = None,
) -> EvalRun:
    started_at = time.time()
    run_id = run_id or f"{solver.name}-{int(started_at)}"
    if budget_usd_per_run is None:
        budget_usd_per_run = getattr(solver, "budget_usd_per_run", None)
    results: list[TaskResult] = []

    db = sqlite3.connect(str(db_path or DEFAULT_DB_PATH))
    _init_db(db)

    done: set[str] = set()
    if resume:
        done = {
            row[0]
            for row in db.execute(
                "SELECT task_id FROM task_results WHERE run_id=?", (run_id,)
            )
        }
        prev = db.execute(
            "SELECT started_at FROM runs WHERE run_id=?", (run_id,)
        ).fetchone()
        if prev is not None:  # le run reprend, on garde son horodatage d'origine
            started_at = float(prev[0])
        if verbose and done:
            print(f"  reprise de {run_id} : {len(done)} tâche(s) déjà journalisée(s)")

    def snapshot(status: str) -> EvalRun:
        n_done, n_solved, cost_usd = _run_aggregates(db, run_id)
        run = EvalRun(
            run_id=run_id,
            solver_name=solver.name,
            git_sha=_git_sha(),
            split=split,
            score=n_solved / len(tasks) if tasks else 0.0,
            n_tasks=len(tasks),
            n_solved=n_solved,
            cost_usd=cost_usd,
            duration_s=time.time() - started_at,
            results=results,
            status=status,
            n_done=n_done,
        )
        _write_run_row(db, run, started_at, timeout_s)
        return run

    run = snapshot("partial")  # le run existe dans runs.db avant la 1re tâche
    for task in tasks:
        if task.task_id in done:
            continue
        if budget_usd_per_run is not None and run.cost_usd >= budget_usd_per_run:
            if verbose:
                print(
                    f"  plafond global atteint : {run.cost_usd:.4f} USD >= "
                    f"{budget_usd_per_run} USD — arrêt propre "
                    f"({run.n_done}/{run.n_tasks} tâches faites)"
                )
            run = snapshot("budget_stop")
            db.close()
            return run
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
        result = TaskResult(
            task_id=task.task_id,
            status=status,
            duration_s=time.time() - t0,
            cost_usd=float(meta.get("cost_usd", 0.0)),
            n_attempts=n_attempts,
            meta=extra_meta,
        )
        results.append(result)
        # écriture au fil de l'eau : un kill ne perd que la tâche en cours
        _write_task_result(db, run_id, result)
        run = snapshot("partial")
        if verbose:
            print(f"  {task.task_id}: {status} ({result.duration_s:.1f}s)")

    run = snapshot("complete")
    db.close()
    return run
