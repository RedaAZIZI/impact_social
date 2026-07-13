"""DSL minimale : 10 primitives Grid -> Grid, interpréteur, brute-force (X-55).

Une hypothèse = composition séquentielle de 1 à 3 primitives. La recherche
exhaustive garde les programmes qui reproduisent exactement TOUTES les paires
d'entraînement ; départage MDL embryonnaire : programme le plus court, puis
ordre lexicographique — déterminisme total.
"""

from __future__ import annotations

import signal
from collections.abc import Callable
from dataclasses import dataclass
from itertools import product

import numpy as np

from solveur.data.loader import Grid, Task

PROGRAM_TIMEOUT_S = 0.1  # 100 ms par exécution de programme
MAX_DEPTH = 3

# -- les 10 primitives ------------------------------------------------------


def rotate90(g: Grid) -> Grid:
    return np.rot90(g)


def rotate180(g: Grid) -> Grid:
    return np.rot90(g, 2)


def flip_h(g: Grid) -> Grid:
    return np.fliplr(g)


def flip_v(g: Grid) -> Grid:
    return np.flipud(g)


def transpose(g: Grid) -> Grid:
    return g.T


def crop_to_content(g: Grid) -> Grid:
    """Rogne au plus petit rectangle contenant les cellules non nulles."""
    nonzero = np.argwhere(g != 0)
    if nonzero.size == 0:
        return g
    (r0, c0), (r1, c1) = nonzero.min(axis=0), nonzero.max(axis=0)
    return g[r0 : r1 + 1, c0 : c1 + 1]


def recolor(a: int, b: int) -> Callable[[Grid], Grid]:
    def apply(g: Grid) -> Grid:
        out = g.copy()
        out[g == a] = b
        return out

    apply.__name__ = f"recolor({a}->{b})"
    return apply


def tile(nx: int, ny: int) -> Callable[[Grid], Grid]:
    def apply(g: Grid) -> Grid:
        return np.tile(g, (ny, nx))

    apply.__name__ = f"tile({nx},{ny})"
    return apply


def scale(k: int) -> Callable[[Grid], Grid]:
    def apply(g: Grid) -> Grid:
        return np.kron(g, np.ones((k, k), dtype=g.dtype))

    apply.__name__ = f"scale({k})"
    return apply


def identity(g: Grid) -> Grid:
    return g


# Fabriques paramétrées instanciées par tâche ; primitives simples telles quelles.
PRIMITIVE_FACTORIES = {
    "rotate90": rotate90,
    "rotate180": rotate180,
    "flip_h": flip_h,
    "flip_v": flip_v,
    "transpose": transpose,
    "crop_to_content": crop_to_content,
    "recolor": recolor,  # instancié sur les paires de couleurs de la tâche
    "tile": tile,  # instancié sur (2,1), (1,2), (2,2), (3,3)
    "scale": scale,  # instancié sur k=2,3
    "identity": identity,
}

TILE_PARAMS = [(2, 1), (1, 2), (2, 2), (3, 3)]
SCALE_PARAMS = [2, 3]

Primitive = Callable[[Grid], Grid]
Program = tuple[str, ...]  # noms des primitives instanciées, dans l'ordre


def instantiate_primitives(task: Task) -> dict[str, Primitive]:
    """Primitives concrètes pour une tâche : recolor sur ses couleurs présentes."""
    prims: dict[str, Primitive] = {
        name: fn  # type: ignore[misc]
        for name, fn in PRIMITIVE_FACTORIES.items()
        if name not in ("recolor", "tile", "scale")
    }
    colors: set[int] = set()
    for grid_in, grid_out in task.train_pairs:
        colors |= set(np.unique(grid_in).tolist()) | set(np.unique(grid_out).tolist())
    for a, b in product(sorted(colors), sorted(colors)):
        if a != b:
            prims[f"recolor({a}->{b})"] = recolor(a, b)
    for nx, ny in TILE_PARAMS:
        prims[f"tile({nx},{ny})"] = tile(nx, ny)
    for k in SCALE_PARAMS:
        prims[f"scale({k})"] = scale(k)
    return prims


def enumerate_programs(primitive_names: list[str], max_depth: int = MAX_DEPTH) -> list[Program]:
    """Toutes les compositions de 1 à max_depth primitives (ordre déterministe)."""
    names = sorted(primitive_names)
    programs: list[Program] = []
    for depth in range(1, max_depth + 1):
        programs.extend(product(names, repeat=depth))
    return programs


class _ProgramTimeout(Exception):
    pass


def run_program(program: Program, prims: dict[str, Primitive], grid: Grid) -> Grid | None:
    """Exécute une composition avec timeout 100 ms. None si erreur/timeout/grille invalide."""

    def _raise(_sig: int, _frame: object) -> None:
        raise _ProgramTimeout

    old = signal.signal(signal.SIGALRM, _raise)
    signal.setitimer(signal.ITIMER_REAL, PROGRAM_TIMEOUT_S)
    try:
        out = grid
        for name in program:
            out = prims[name](out)
            if out.size == 0 or out.shape[0] > 30 or out.shape[1] > 30:
                return None
        return np.ascontiguousarray(out, dtype=np.int8)
    except (_ProgramTimeout, Exception):
        return None
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


@dataclass
class SearchResult:
    program: Program | None
    n_candidates: int
    n_survivors: int


def search(task: Task, max_depth: int = MAX_DEPTH) -> SearchResult:
    """Recherche exhaustive : programmes reproduisant exactement tout le train.

    Départage : plus court d'abord, puis ordre lexicographique (l'énumération
    est déjà triée ainsi — on prend le premier survivant).
    """
    prims = instantiate_primitives(task)
    programs = enumerate_programs(list(prims), max_depth)
    survivors: list[Program] = []
    for program in programs:
        ok = True
        for grid_in, grid_out in task.train_pairs:
            result = run_program(program, prims, grid_in)
            if (
                result is None
                or result.shape != grid_out.shape
                or not np.array_equal(result, grid_out)
            ):
                ok = False
                break
        if ok:
            survivors.append(program)
    return SearchResult(
        program=survivors[0] if survivors else None,
        n_candidates=len(programs),
        n_survivors=len(survivors),
    )


class BruteForceSolver:
    """Baseline 2 : brute-force sur la DSL, branchée sur le runner (X-52)."""

    name = "brute"

    def __init__(self, max_depth: int = MAX_DEPTH, **_kw: object) -> None:
        self.max_depth = max_depth
        self.meta: dict[str, object] = {}

    def solve(self, task: Task) -> list[list[Grid]]:
        result = search(task, self.max_depth)
        self.meta = {
            "program": list(result.program) if result.program else None,
            "n_candidates": result.n_candidates,
            "n_survivors": result.n_survivors,
        }
        if result.program is None:
            return [[] for _ in task.test_pairs]
        prims = instantiate_primitives(task)
        attempts: list[list[Grid]] = []
        for test_in, _expected in task.test_pairs:
            out = run_program(result.program, prims, test_in)
            attempts.append([out] if out is not None else [])
        return attempts
