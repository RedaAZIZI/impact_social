"""Registre des solveurs branchés sur le runner (X-52+).

Chaque baseline (X-54, X-55) s'enregistre ici pour être accessible par
`python -m solveur.eval --solver <name>`.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from solveur.data.loader import Grid, Task


class RandomSolver:
    """Solveur aléatoire — sert de référence ~0% et de test du runner."""

    name = "random"

    def __init__(self, seed: int = 0) -> None:
        self.seed = seed

    def solve(self, task: Task) -> list[list[Grid]]:
        rng = np.random.default_rng(self.seed)
        out: list[list[Grid]] = []
        for test_in, _expected in task.test_pairs:
            out.append(
                [rng.integers(0, 10, size=test_in.shape, dtype=np.int8) for _ in range(2)]
            )
        return out


_BUILDERS: dict[str, Any] = {
    "random": lambda **_kw: RandomSolver(),
}


def register_solver(name: str, builder: Any) -> None:
    _BUILDERS[name] = builder


def list_solvers() -> list[str]:
    return sorted(_BUILDERS)


def build_solver(name: str, **kwargs: Any) -> Any:
    return _BUILDERS[name](**kwargs)
