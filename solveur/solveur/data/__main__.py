"""CLI : python -m solveur.data --stats (X-51).

Affiche les comptes par split et la distribution des tailles de grilles.
Le split final n'est jamais chargé : seul son compte (issu de splits.json)
est affiché.
"""

from __future__ import annotations

import argparse
from collections import Counter

from solveur.data.loader import get_split, load_splits


def _grid_size_distribution(split: str) -> Counter[str]:
    sizes: Counter[str] = Counter()
    for task in get_split(split):
        for grid_in, grid_out in task.train_pairs + task.test_pairs:
            sizes[f"{grid_in.shape[0]}x{grid_in.shape[1]}"] += 1
            sizes[f"{grid_out.shape[0]}x{grid_out.shape[1]}"] += 1
    return sizes


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m solveur.data")
    parser.add_argument("--stats", action="store_true", help="comptes et tailles de grilles")
    args = parser.parse_args()
    if not args.stats:
        parser.print_help()
        return

    meta = load_splits()
    print(f"Splits scellés (seed={meta['seed']}) :")
    for name, count in meta["counts"].items():
        print(f"  {name:<12} {count} tâches")
    for split in ("dev", "validation"):
        sizes = _grid_size_distribution(split)
        top = ", ".join(f"{s}×{n}" for s, n in sizes.most_common(8))
        print(f"\nTailles de grilles ({split}, top 8) : {top}")
    print("\n(le split final est scellé — comptes uniquement, jamais chargé)")


if __name__ == "__main__":
    main()
