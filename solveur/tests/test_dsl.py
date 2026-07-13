"""X-55 — critères d'acceptation de la DSL et du brute-force."""

from __future__ import annotations

import numpy as np
import pytest

from solveur.data.loader import Task
from solveur.dsl.core import (
    BruteForceSolver,
    crop_to_content,
    enumerate_programs,
    flip_h,
    flip_v,
    identity,
    instantiate_primitives,
    recolor,
    rotate90,
    rotate180,
    run_program,
    scale,
    search,
    tile,
    transpose,
)

G = lambda rows: np.array(rows, dtype=np.int8)  # noqa: E731

CELL = G([[7]])  # 1×1
RECT = G([[1, 2, 3], [4, 5, 6]])  # 2×3 non-carré
SQUARE = G([[1, 2], [3, 4]])


class TestPrimitives:
    """≥3 cas par primitive, incluant 1×1 et non-carré."""

    @pytest.mark.parametrize(
        ("fn", "grid", "expected"),
        [
            (rotate90, CELL, [[7]]),
            (rotate90, SQUARE, [[2, 4], [1, 3]]),
            (rotate90, RECT, [[3, 6], [2, 5], [1, 4]]),
            (rotate180, CELL, [[7]]),
            (rotate180, SQUARE, [[4, 3], [2, 1]]),
            (rotate180, RECT, [[6, 5, 4], [3, 2, 1]]),
            (flip_h, CELL, [[7]]),
            (flip_h, SQUARE, [[2, 1], [4, 3]]),
            (flip_h, RECT, [[3, 2, 1], [6, 5, 4]]),
            (flip_v, CELL, [[7]]),
            (flip_v, SQUARE, [[3, 4], [1, 2]]),
            (flip_v, RECT, [[4, 5, 6], [1, 2, 3]]),
            (transpose, CELL, [[7]]),
            (transpose, SQUARE, [[1, 3], [2, 4]]),
            (transpose, RECT, [[1, 4], [2, 5], [3, 6]]),
            (identity, CELL, [[7]]),
            (identity, SQUARE, [[1, 2], [3, 4]]),
            (identity, RECT, [[1, 2, 3], [4, 5, 6]]),
            (crop_to_content, G([[0, 0], [0, 5]]), [[5]]),
            (crop_to_content, G([[0, 0, 0], [0, 1, 2], [0, 3, 4]]), [[1, 2], [3, 4]]),
            (crop_to_content, G([[0]]), [[0]]),  # tout vide : inchangé
            (recolor(1, 9), CELL, [[7]]),
            (recolor(1, 9), SQUARE, [[9, 2], [3, 4]]),
            (recolor(5, 0), RECT, [[1, 2, 3], [4, 0, 6]]),
            (tile(2, 1), CELL, [[7, 7]]),
            (tile(1, 2), CELL, [[7], [7]]),
            (tile(2, 2), SQUARE, [[1, 2, 1, 2], [3, 4, 3, 4], [1, 2, 1, 2], [3, 4, 3, 4]]),
            (scale(2), CELL, [[7, 7], [7, 7]]),
            (scale(2), SQUARE, [[1, 1, 2, 2], [1, 1, 2, 2], [3, 3, 4, 4], [3, 3, 4, 4]]),
            (scale(3), CELL, [[7]] and [[7, 7, 7], [7, 7, 7], [7, 7, 7]]),
        ],
    )
    def test_primitive(self, fn, grid, expected):  # type: ignore[no-untyped-def]
        assert np.array_equal(fn(grid), G(expected))


def test_composition_count() -> None:
    names = [f"p{i}" for i in range(5)]
    programs = enumerate_programs(names, max_depth=3)
    assert len(programs) == 5 + 5**2 + 5**3  # n + n² + n³


def make_task(train, test):  # type: ignore[no-untyped-def]
    return Task(
        task_id="mock/dsl",
        source="mock",
        train_pairs=[(G(a), G(b)) for a, b in train],
        test_pairs=[(G(a), G(b)) for a, b in test],
    )


def test_search_finds_symmetry() -> None:
    # transformation = rotate180
    task = make_task(
        train=[([[1, 2], [3, 4]], [[4, 3], [2, 1]]), ([[5, 0], [0, 0]], [[0, 0], [0, 5]])],
        test=[([[1, 0], [0, 2]], [[2, 0], [0, 1]])],
    )
    result = search(task)
    assert result.program is not None
    prims = instantiate_primitives(task)
    out = run_program(result.program, prims, task.test_pairs[0][0])
    assert np.array_equal(out, task.test_pairs[0][1])


def test_mdl_shortest_first() -> None:
    # un programme de profondeur 1 doit gagner face à flip_h∘flip_h (profondeur 2),
    # départagé par ordre lexicographique (crop_to_content < identity, tous deux valides)
    task = make_task(train=[([[1, 2]], [[1, 2]])], test=[([[3, 4]], [[3, 4]])])
    result = search(task)
    assert result.program is not None and len(result.program) == 1
    assert result.program == ("crop_to_content",)  # premier survivant lexicographique


def test_determinism() -> None:
    task = make_task(
        train=[([[1, 2], [3, 4]], [[2, 1], [4, 3]])],
        test=[([[5, 6], [7, 8]], [[6, 5], [8, 7]])],
    )
    solver = BruteForceSolver()
    runs = [solver.solve(task) for _ in range(2)]
    for a, b in zip(*runs, strict=True):
        assert len(a) == len(b)
        for ga, gb in zip(a, b, strict=True):
            assert np.array_equal(ga, gb)
    r1, r2 = search(task), search(task)
    assert r1.program == r2.program and r1.n_survivors == r2.n_survivors
