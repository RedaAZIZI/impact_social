"""Génération de rapports Markdown depuis runs.db (X-56).

- Rapport simple : score, coût, durée, répartition des statuts, régressions
  vs le run précédent du même solveur, taxonomie d'échecs v0, 5 échecs
  visualisés (input / attendu / produit).
- Comparatif : tableau côte à côte, deltas, ensembles A-seul / B-seul / commun.
"""

from __future__ import annotations

import json
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

from solveur.data.loader import Grid, Task

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = PROJECT_ROOT / "runs.db"
REPORTS_DIR = PROJECT_ROOT / "reports"

# rendu emoji des couleurs ARC 0-9
_EMOJI = ["⬛", "🟦", "🟥", "🟩", "🟨", "⬜", "🟪", "🟧", "🟫", "🟠"]


def render_grid(grid: Grid | list[list[int]] | None) -> str:
    if grid is None:
        return "(aucune sortie)"
    arr = np.asarray(grid)
    return "\n".join("".join(_EMOJI[int(v)] for v in row) for row in arr)


def classify_failure(expected: Grid, produced: Grid | list[list[int]] | None) -> str:
    """Taxonomie v0 : heuristiques simples pour amorcer l'analyse des échecs."""
    if produced is None:
        return "no_output"
    produced = np.asarray(produced)
    if produced.shape != expected.shape:
        return "wrong_size"
    if set(np.unique(produced).tolist()) != set(np.unique(expected).tolist()):
        return "wrong_colors"
    hamming = float(np.mean(produced != expected))
    return "near_miss" if hamming <= 0.10 else "far"


def _fetch_run(db: sqlite3.Connection, run_id: str) -> dict[str, Any]:
    row = db.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
    if row is None:
        raise KeyError(f"run inconnu : {run_id!r}")
    cols = [c[0] for c in db.execute("SELECT * FROM runs LIMIT 0").description]
    return dict(zip(cols, row, strict=True))


def _fetch_results(db: sqlite3.Connection, run_id: str) -> dict[str, dict[str, Any]]:
    rows = db.execute(
        "SELECT task_id, status, duration_s, cost_usd, n_attempts, meta_json "
        "FROM task_results WHERE run_id = ? ORDER BY task_id",
        (run_id,),
    ).fetchall()
    return {
        r[0]: {
            "status": r[1],
            "duration_s": r[2],
            "cost_usd": r[3],
            "n_attempts": r[4],
            "meta": json.loads(r[5] or "{}"),
        }
        for r in rows
    }


def _solved_set(results: dict[str, dict[str, Any]]) -> set[str]:
    return {tid for tid, r in results.items() if r["status"] == "solved"}


def _previous_run_id(db: sqlite3.Connection, run: dict[str, Any]) -> str | None:
    row = db.execute(
        "SELECT run_id FROM runs WHERE solver_name = ? AND split = ? AND started_at < ? "
        "ORDER BY started_at DESC LIMIT 1",
        (run["solver_name"], run["split"], run["started_at"]),
    ).fetchone()
    return row[0] if row else None


def _first_attempt(meta: dict[str, Any]) -> list[list[int]] | None:
    attempts = meta.get("attempts") or []
    for per_test in attempts:
        if per_test:
            return per_test[0]
    return None


def _load_tasks_by_id(task_ids: list[str]) -> dict[str, Task]:
    from solveur.data.loader import load_all_tasks

    try:
        all_tasks = load_all_tasks()
    except Exception:
        return {}
    return {tid: all_tasks[tid] for tid in task_ids if tid in all_tasks}


def run_report(
    run_id: str, db_path: Path | str | None = None, out_dir: Path | str | None = None
) -> Path:
    db = sqlite3.connect(str(db_path or DEFAULT_DB_PATH))
    run = _fetch_run(db, run_id)
    results = _fetch_results(db, run_id)
    statuses = Counter(r["status"] for r in results.values())
    n = len(results) or 1

    lines = [
        f"# Rapport de run — `{run_id}`",
        "",
        f"- **Solveur** : {run['solver_name']}",
        f"- **Split** : {run['split']} — **git_sha** : `{run['git_sha']}`",
        f"- **Score** : **{run['score']:.1%}** ({run['n_solved']}/{run['n_tasks']})",
        f"- **Coût** : {run['cost_usd']:.4f} USD total — {run['cost_usd'] / n:.5f} USD/tâche",
        f"- **Durée** : {run['duration_s']:.0f} s ({run['duration_s'] / n:.1f} s/tâche)",
        "",
        "## Répartition des statuts",
        "",
        "| statut | tâches |",
        "|---|---|",
    ]
    for status, count in statuses.most_common():
        lines.append(f"| {status} | {count} |")

    # -- régressions vs run précédent du même solveur ------------------------
    lines += ["", "## Régressions vs run précédent"]
    prev_id = _previous_run_id(db, run)
    if prev_id is None:
        lines += ["", "Pas de run précédent pour ce solveur sur ce split."]
    else:
        prev_solved = _solved_set(_fetch_results(db, prev_id))
        cur_solved = _solved_set(results)
        lost, gained = sorted(prev_solved - cur_solved), sorted(cur_solved - prev_solved)
        lines += ["", f"Comparé à `{prev_id}` :", ""]
        lines.append(f"- **Régressions (perdues)** : {', '.join(lost) or 'aucune'}")
        lines.append(f"- **Gagnées** : {', '.join(gained) or 'aucune'}")

    # -- taxonomie d'échecs v0 ----------------------------------------------
    failed = {tid: r for tid, r in results.items() if r["status"] != "solved"}
    tasks = _load_tasks_by_id(list(failed))
    taxonomy: Counter[str] = Counter()
    labeled: dict[str, str] = {}
    for tid, r in failed.items():
        if tid in tasks:
            expected = tasks[tid].test_pairs[0][1]
            label = classify_failure(expected, _first_attempt(r["meta"]))
        else:
            label = r["status"] if r["status"] in ("timeout", "crash") else "no_output"
        taxonomy[label] += 1
        labeled[tid] = label

    lines += ["", "## Taxonomie d'échecs v0", "", "| catégorie | tâches |", "|---|---|"]
    for label, count in taxonomy.most_common():
        lines.append(f"| {label} | {count} |")

    # -- 5 échecs échantillonnés ---------------------------------------------
    lines += ["", "## Échantillon d'échecs (5)"]
    for tid in sorted(failed)[:5]:
        lines += ["", f"### `{tid}` — {failed[tid]['status']} / {labeled.get(tid, '?')}", ""]
        if tid in tasks:
            test_in, expected = tasks[tid].test_pairs[0]
            produced = _first_attempt(failed[tid]["meta"])
            lines += [
                "Input :", "", render_grid(test_in), "",
                "Attendu :", "", render_grid(expected), "",
                "Produit :", "", render_grid(produced), "",
            ]
        else:
            lines += ["", "(tâche non trouvée dans le dataset local)"]

    out_dir = Path(out_dir or REPORTS_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"run_{run_id}.md"
    out_path.write_text("\n".join(lines) + "\n")
    db.close()
    return out_path


def compare_report(
    run_a: str, run_b: str, db_path: Path | str | None = None, out_dir: Path | str | None = None
) -> Path:
    db = sqlite3.connect(str(db_path or DEFAULT_DB_PATH))
    a, b = _fetch_run(db, run_a), _fetch_run(db, run_b)
    res_a, res_b = _fetch_results(db, run_a), _fetch_results(db, run_b)
    solved_a, solved_b = _solved_set(res_a), _solved_set(res_b)
    only_a, only_b = sorted(solved_a - solved_b), sorted(solved_b - solved_a)
    both = sorted(solved_a & solved_b)

    lines = [
        f"# Comparatif — `{run_a}` vs `{run_b}`",
        "",
        "| | " + f"`{run_a}` | `{run_b}` | Δ |",
        "|---|---|---|---|",
        f"| solveur | {a['solver_name']} | {b['solver_name']} | |",
        f"| score | {a['score']:.1%} | {b['score']:.1%} | {b['score'] - a['score']:+.1%} |",
        f"| résolues | {a['n_solved']}/{a['n_tasks']} | {b['n_solved']}/{b['n_tasks']} | |",
        (
            f"| coût USD | {a['cost_usd']:.4f} | {b['cost_usd']:.4f} "
            f"| {b['cost_usd'] - a['cost_usd']:+.4f} |"
        ),
        f"| durée s | {a['duration_s']:.0f} | {b['duration_s']:.0f} | |",
        "",
        "## Ensembles de tâches résolues",
        "",
        f"- **{run_a} seul** ({len(only_a)}) : {', '.join(only_a) or '—'}",
        f"- **{run_b} seul** ({len(only_b)}) : {', '.join(only_b) or '—'}",
        f"- **Les deux** ({len(both)}) : {', '.join(both) or '—'}",
    ]

    out_dir = Path(out_dir or REPORTS_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"compare_{run_a}_vs_{run_b}.md"
    out_path.write_text("\n".join(lines) + "\n")
    db.close()
    return out_path
