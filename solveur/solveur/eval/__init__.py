"""X-52 — runner d'évaluation sandboxé, scoring officiel ARC, tracking SQLite."""

from solveur.eval.runner import (
    EvalRun,
    Solver,
    TaskResult,
    grids_equal,
    run_eval,
)

__all__ = ["EvalRun", "Solver", "TaskResult", "grids_equal", "run_eval"]
