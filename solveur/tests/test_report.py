"""X-56 — critères d'acceptation des rapports."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from solveur.data.loader import Grid, Task
from solveur.eval.runner import run_eval
from solveur.report.report import classify_failure, compare_report, run_report

G = lambda rows: np.array(rows, dtype=np.int8)  # noqa: E731


def make_task(i: int) -> Task:
    grid_in = G([[i % 10, (i + 1) % 10], [(i + 2) % 10, (i + 3) % 10]])
    grid_out = np.rot90(grid_in).copy()
    return Task(f"mock/{i}", "mock", [(grid_in, grid_out)], [(grid_in, grid_out)])


TASKS = [make_task(i) for i in range(6)]


class SubsetSolver:
    """Résout les tâches dont l'indice est dans `solvable` — nom configurable."""

    def __init__(self, name: str, solvable: set[int]) -> None:
        self.name = name
        self.solvable = solvable

    def solve(self, task: Task) -> list[list[Grid]]:
        idx = int(task.task_id.split("/")[-1])
        if idx in self.solvable:
            return [[expected] for _in, expected in task.test_pairs]
        return [[np.zeros_like(expected)] for _in, expected in task.test_pairs]


def test_report_generated(tmp_path: Path) -> None:
    db = tmp_path / "runs.db"
    run_eval(SubsetSolver("s1", {0, 1}), TASKS, split="mock", run_id="r1", db_path=db)
    path = run_report("r1", db_path=db, out_dir=tmp_path / "reports")
    text = path.read_text()
    for section in (
        "# Rapport de run",
        "**Score**",
        "Coût",
        "Durée",
        "## Répartition des statuts",
        "## Régressions vs run précédent",
        "## Taxonomie d'échecs v0",
        "## Échantillon d'échecs",
    ):
        assert section in text, f"section manquante : {section}"


def test_regression_detection(tmp_path: Path) -> None:
    db = tmp_path / "runs.db"
    run_eval(SubsetSolver("s1", {0, 1, 2}), TASKS, split="mock", run_id="n-1", db_path=db)
    run_eval(SubsetSolver("s1", {0, 3}), TASKS, split="mock", run_id="n", db_path=db)
    text = run_report("n", db_path=db, out_dir=tmp_path / "reports").read_text()
    regress_line = next(line for line in text.splitlines() if "Régressions (perdues)" in line)
    assert "mock/1" in regress_line and "mock/2" in regress_line
    gained_line = next(line for line in text.splitlines() if "Gagnées" in line)
    assert "mock/3" in gained_line


def test_compare(tmp_path: Path) -> None:
    db = tmp_path / "runs.db"
    run_eval(SubsetSolver("a", {0, 1, 2}), TASKS, split="mock", run_id="run-a", db_path=db)
    run_eval(SubsetSolver("b", {2, 3}), TASKS, split="mock", run_id="run-b", db_path=db)
    text = compare_report("run-a", "run-b", db_path=db, out_dir=tmp_path / "reports").read_text()
    only_a = next(line for line in text.splitlines() if "run-a seul" in line)
    only_b = next(line for line in text.splitlines() if "run-b seul" in line)
    both = next(line for line in text.splitlines() if "Les deux" in line)
    assert "mock/0" in only_a and "mock/1" in only_a and "mock/2" not in only_a
    assert "mock/3" in only_b
    assert "mock/2" in both


def test_taxonomy() -> None:
    expected = G([[1, 2], [3, 4]])
    assert classify_failure(expected, None) == "no_output"
    assert classify_failure(expected, G([[1, 2, 3]])) == "wrong_size"
    assert classify_failure(expected, G([[1, 2], [3, 9]])) == "wrong_colors"
    big = np.tile(expected, (5, 5))
    near = big.copy()
    near[0, 0] = (near[0, 0] + 1) % 4 + 1  # 1 cellule sur 100, couleurs conservées
    assert classify_failure(big, near) == "near_miss"
    assert classify_failure(expected, G([[4, 3], [2, 1]])) == "far"
