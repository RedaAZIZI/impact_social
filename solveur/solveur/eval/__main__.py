"""CLI : python -m solveur.eval --solver <name> --split dev (X-52, X-61)."""

from __future__ import annotations

import argparse
from collections import Counter

from solveur.data.loader import get_split
from solveur.eval.runner import DEFAULT_TIMEOUT_S, run_eval
from solveur.solvers import build_solver, list_solvers


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m solveur.eval")
    parser.add_argument("--solver", required=True, choices=list_solvers())
    parser.add_argument("--split", default="dev", help="dev | validation")
    parser.add_argument("--run-id", default=None, help="identifiant du run (défaut auto)")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_S)
    parser.add_argument("--limit", type=int, default=None, help="nombre max de tâches")
    parser.add_argument("--no-cache", action="store_true", help="désactive le cache oracle")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="reprend le run --run-id : saute les tâches déjà dans runs.db",
    )
    parser.add_argument(
        "--budget-usd-per-run",
        type=float,
        default=None,
        help="plafond global du run en USD (défaut : budget_usd_per_run de la config solveur)",
    )
    args = parser.parse_args()
    if args.resume and not args.run_id:
        parser.error("--resume exige --run-id (le run à reprendre)")

    tasks = get_split(args.split)
    if args.limit:
        tasks = tasks[: args.limit]
    solver = build_solver(args.solver, use_cache=not args.no_cache)
    run = run_eval(solver, tasks, split=args.split, run_id=args.run_id,
                   timeout_s=args.timeout, verbose=True, resume=args.resume,
                   budget_usd_per_run=args.budget_usd_per_run)

    statuses = Counter(r.status for r in run.results)
    print(f"\nRun {run.run_id} — solveur {run.solver_name} — split {run.split}")
    print(f"  git_sha : {run.git_sha}")
    print(f"  statut  : {run.status} ({run.n_done}/{run.n_tasks} tâches faites)")
    print(f"  score   : {run.score:.1%} ({run.n_solved}/{run.n_tasks})")
    print(f"  coût    : {run.cost_usd:.4f} USD")
    print(f"  durée   : {run.duration_s:.0f}s")
    print(f"  statuts : {dict(statuses)}")
    print("  → écrit dans runs.db")


if __name__ == "__main__":
    main()
