"""CLI : python -m solveur.report --run <run_id> | --compare <a> <b> | --latest (X-56)."""

from __future__ import annotations

import argparse
import sqlite3

from solveur.report.report import DEFAULT_DB_PATH, compare_report, run_report


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m solveur.report")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", help="génère le rapport d'un run")
    group.add_argument("--compare", nargs=2, metavar=("RUN_A", "RUN_B"))
    group.add_argument("--latest", action="store_true", help="rapport du dernier run (hook CI)")
    group.add_argument(
        "--taxonomy",
        action="store_true",
        help="taxonomie des échecs des runs officiels EPIC-0 (X-60)",
    )
    parser.add_argument("--db", default=None, help="chemin de runs.db")
    args = parser.parse_args()

    if args.taxonomy:
        from solveur.report.taxonomy import taxonomy_report

        path = taxonomy_report(db_path=args.db)
    elif args.latest:
        db = sqlite3.connect(str(args.db or DEFAULT_DB_PATH))
        row = db.execute("SELECT run_id FROM runs ORDER BY started_at DESC LIMIT 1").fetchone()
        db.close()
        if row is None:
            print("Aucun run dans runs.db — rien à faire.")
            return
        path = run_report(row[0], db_path=args.db)
    elif args.run:
        path = run_report(args.run, db_path=args.db)
    else:
        run_a, run_b = args.compare
        path = compare_report(run_a, run_b, db_path=args.db)
    print(f"Rapport écrit : {path}")


if __name__ == "__main__":
    main()
