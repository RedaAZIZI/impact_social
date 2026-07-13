"""X-60 — critères d'acceptation de la taxonomie des échecs (aucun appel API)."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import numpy as np

from solveur.data.loader import Task
from solveur.report.taxonomy import (
    CATEGORIES,
    categorize,
    categorize_run,
    recommend_primitives,
    taxonomy_report,
)

G = lambda rows: np.array(rows, dtype=np.int8)  # noqa: E731


# --- catégorisation unitaire --------------------------------------------------


def test_categorize_statuses() -> None:
    expected = G([[1, 2], [3, 4]])
    assert categorize("parse_error", expected, None) == "parse_error"
    assert categorize("timeout", expected, None) == "timeout"
    assert categorize("failed", expected, None) == "structure_missed"


def test_categorize_grids() -> None:
    expected = G([[1, 2, 3, 4, 5]] * 5)
    assert categorize("failed", expected, G([[1, 2], [3, 4]])) == "wrong_size"
    near = expected.copy()
    near[0, 0] = 2  # 1/25 = 4 % < 5 %
    assert categorize("failed", expected, near) == "near_miss"
    assert categorize("failed", expected, np.full_like(expected, 7)) == "wrong_colors"
    shuffled = expected[::-1].copy()  # mêmes couleurs, structure ratée
    shuffled[0], shuffled[1] = expected[1].copy(), expected[0].copy()
    assert categorize("failed", expected, np.rot90(expected).T[::-1]) in CATEGORIES


def test_partition_exactly_one_category() -> None:
    """Chaque tâche échouée reçoit exactement une catégorie de CATEGORIES."""
    tasks = {}
    results = {}
    statuses = ["failed", "timeout", "parse_error", "failed", "failed", "solved"]
    for i, status in enumerate(statuses):
        tid = f"mock/{i}"
        grid_in = G([[i % 10, 1], [2, 3]])
        expected = np.rot90(grid_in).copy()
        tasks[tid] = Task(tid, "mock", [(grid_in, expected)], [(grid_in, expected)])
        produced = expected.tolist() if i % 2 else [[0]]
        results[tid] = {
            "status": status,
            "meta": {"attempts": [[produced]]},
        }
    labels = categorize_run(results, tasks)
    failed_ids = {tid for tid, r in results.items() if r["status"] != "solved"}
    assert set(labels) == failed_ids  # toutes les échouées, aucune résolue
    for tid, label in labels.items():
        assert label in CATEGORIES, f"{tid} hors partition : {label}"


# --- détecteurs de primitives -------------------------------------------------


def test_recommend_primitives_detects_and_caps() -> None:
    tasks = {}
    # recolor_map : mapping couleur→couleur pixel à pixel
    inp = G([[1, 2], [2, 1]])
    tasks["mock/recolor"] = Task(
        "mock/recolor", "mock", [], [(inp, G([[4, 5], [5, 4]]))]
    )
    # extract_object : crop d'une composante connexe
    inp2 = G([[0, 0, 0, 0], [0, 3, 3, 0], [0, 3, 3, 0], [0, 0, 0, 0]])
    tasks["mock/object"] = Task(
        "mock/object", "mock", [], [(inp2, G([[3, 3], [3, 3]]))]
    )
    ranked = recommend_primitives(set(tasks), tasks)
    names = [name for name, _cat, _n in ranked]
    assert any("recolor_map" in n for n in names)
    assert any("extract_object" in n for n in names)
    assert len(ranked) <= 10
    for _name, _cat, n in ranked:
        assert n >= 1


# --- rapport de bout en bout ---------------------------------------------------


def _insert_run(db: sqlite3.Connection, run_id: str, rows: list[tuple]) -> None:
    db.execute(
        "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (run_id, run_id, "sha", "dev", "2026-07-13", 0.0, len(rows), 0, 0.0, 1.0),
    )
    for tid, status, meta in rows:
        db.execute(
            "INSERT INTO task_results VALUES (?, ?, ?, ?, ?, ?, ?)",
            (run_id, tid, status, 1.0, 0.0, 1, json.dumps(meta)),
        )


def test_taxonomy_report_written(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "runs.db"
    db = sqlite3.connect(db_path)
    db.execute(
        "CREATE TABLE runs (run_id TEXT PRIMARY KEY, solver_name TEXT, git_sha TEXT,"
        " split TEXT, started_at TEXT, score REAL, n_tasks INT, n_solved INT,"
        " cost_usd REAL, duration_s REAL)"
    )
    db.execute(
        "CREATE TABLE task_results (run_id TEXT, task_id TEXT, status TEXT,"
        " duration_s REAL, cost_usd REAL, n_attempts INT, meta_json TEXT,"
        " PRIMARY KEY (run_id, task_id))"
    )
    grid_in = G([[1, 2], [2, 1]])
    expected = G([[4, 5], [5, 4]])
    task = Task("mock/0", "mock", [], [(grid_in, expected)])
    rows = [
        ("mock/0", "failed", {"attempts": [[[[0]]]]}),
        ("mock/1", "timeout", {}),
    ]
    for rid in ("run-a", "run-b"):
        _insert_run(db, rid, rows)
    db.commit()
    db.close()

    monkeypatch.setattr(
        "solveur.report.taxonomy._load_tasks_by_id", lambda ids: {"mock/0": task}
    )
    out = taxonomy_report(("run-a", "run-b"), db_path=db_path, out_dir=tmp_path)
    assert out.exists()
    text = out.read_text()
    assert "Masses par catégorie" in text
    assert "Primitives DSL v1 candidates" in text
    # ≤ 10 primitives recommandées
    section = text.split("Primitives DSL v1 candidates")[1]
    n_rows = sum(1 for line in section.splitlines() if line.startswith("| ") and "---" not in line)
    assert n_rows - 1 <= 10  # -1 pour la ligne d'en-tête
