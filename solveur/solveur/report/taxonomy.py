"""Taxonomie des échecs EPIC-0 (X-60).

Chaque tâche échouée d'un run reçoit exactement une catégorie parmi
`CATEGORIES`. Le rapport `reports/taxonomy_epic0.md` croise les trois runs
officiels (brute-v1, direct-haiku, direct-sonnet), donne les masses par
catégorie, 3 exemples commentés par catégorie, et une recommandation
chiffrée de primitives DSL v1 (chaque primitive candidate est justifiée
par le nombre de tâches échouées qu'un détecteur heuristique estime
qu'elle débloquerait). Aucun appel API : tout vient de runs.db et du
dataset local.
"""

from __future__ import annotations

import sqlite3
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np

from solveur.data.loader import Grid, Task
from solveur.report.report import (
    DEFAULT_DB_PATH,
    REPORTS_DIR,
    _fetch_results,
    _first_attempt,
    _load_tasks_by_id,
)

CATEGORIES = (
    "parse_error",
    "timeout",
    "wrong_size",
    "near_miss",
    "wrong_colors",
    "structure_missed",
)

NEAR_MISS_THRESHOLD = 0.05  # < 5 % de cellules fausses (spec X-60)

OFFICIAL_RUNS = ("brute-v1", "direct-haiku", "direct-sonnet")


def categorize(
    status: str, expected: Grid, produced: Grid | list[list[int]] | None
) -> str:
    """Catégorie unique d'une tâche échouée (partition de CATEGORIES)."""
    if status == "parse_error":
        return "parse_error"
    if status == "timeout":
        return "timeout"
    if produced is None:
        return "structure_missed"
    produced_arr = np.asarray(produced)
    if produced_arr.shape != expected.shape:
        return "wrong_size"
    hamming = float(np.mean(produced_arr != expected))
    if hamming < NEAR_MISS_THRESHOLD:
        return "near_miss"
    if set(np.unique(produced_arr).tolist()) != set(np.unique(expected).tolist()):
        return "wrong_colors"
    return "structure_missed"


def categorize_run(
    results: dict[str, dict[str, Any]], tasks: dict[str, Task]
) -> dict[str, str]:
    """task_id -> catégorie, pour toutes les tâches non résolues d'un run."""
    labels: dict[str, str] = {}
    for tid, r in results.items():
        if r["status"] == "solved":
            continue
        if tid in tasks:
            expected = tasks[tid].test_pairs[0][1]
            labels[tid] = categorize(r["status"], expected, _first_attempt(r["meta"]))
        elif r["status"] in ("timeout", "parse_error"):
            labels[tid] = r["status"]
        else:
            labels[tid] = "structure_missed"
    return labels


# --- détecteurs de primitives candidates -----------------------------------
# Chaque détecteur regarde la première paire de test (input, expected) et
# répond : « la primitive candidate expliquerait-elle plausiblement cette
# transformation ? ». C'est une borne optimiste, pas une résolution.


def _connected_components(grid: Grid, background: int) -> list[np.ndarray]:
    """Masques booléens des composantes 4-connexes non-background."""
    visited = np.zeros(grid.shape, dtype=bool)
    components = []
    h, w = grid.shape
    for si in range(h):
        for sj in range(w):
            if visited[si, sj] or grid[si, sj] == background:
                continue
            mask = np.zeros(grid.shape, dtype=bool)
            stack = [(si, sj)]
            visited[si, sj] = True
            while stack:
                i, j = stack.pop()
                mask[i, j] = True
                for ni, nj in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                    if (
                        0 <= ni < h
                        and 0 <= nj < w
                        and not visited[ni, nj]
                        and grid[ni, nj] != background
                    ):
                        visited[ni, nj] = True
                        stack.append((ni, nj))
            components.append(mask)
    return components


def _bbox_crop(grid: Grid, mask: np.ndarray) -> Grid:
    rows, cols = np.where(mask)
    return grid[rows.min() : rows.max() + 1, cols.min() : cols.max() + 1]


def _detect_recolor_map(inp: Grid, expected: Grid) -> bool:
    """Même forme + application pixel-à-pixel d'une fonction couleur→couleur."""
    if inp.shape != expected.shape or np.array_equal(inp, expected):
        return False
    mapping: dict[int, int] = {}
    for a, b in zip(inp.ravel().tolist(), expected.ravel().tolist(), strict=True):
        if mapping.setdefault(a, b) != b:
            return False
    return True


def _detect_extract_object(inp: Grid, expected: Grid) -> bool:
    """expected == crop d'une composante connexe de l'input (fond = 0)."""
    if expected.size >= inp.size:
        return False
    for mask in _connected_components(inp, background=0):
        crop = _bbox_crop(inp, mask)
        if crop.shape == expected.shape and np.array_equal(crop, expected):
            return True
    return False


def _detect_select_block(inp: Grid, expected: Grid) -> bool:
    """expected est l'un des blocs d'une partition régulière de l'input."""
    ih, iw = inp.shape
    eh, ew = expected.shape
    if eh == 0 or ew == 0 or ih % eh or iw % ew or (ih == eh and iw == ew):
        return False
    for bi in range(ih // eh):
        for bj in range(iw // ew):
            block = inp[bi * eh : (bi + 1) * eh, bj * ew : (bj + 1) * ew]
            if np.array_equal(block, expected):
                return True
    return False


def _detect_tile_transform(inp: Grid, expected: Grid) -> bool:
    """expected pave (k×m > 1) des copies de l'input, éventuellement retournées."""
    ih, iw = inp.shape
    eh, ew = expected.shape
    if ih == 0 or iw == 0 or eh % ih or ew % iw or (eh == ih and ew == iw):
        return False
    variants = [inp, np.flipud(inp), np.fliplr(inp), np.flipud(np.fliplr(inp))]
    for bi in range(eh // ih):
        for bj in range(ew // iw):
            block = expected[bi * ih : (bi + 1) * ih, bj * iw : (bj + 1) * iw]
            if not any(np.array_equal(block, v) for v in variants):
                return False
    return True


def _detect_fill_background(inp: Grid, expected: Grid) -> bool:
    """Seules des cellules de fond (0) de l'input changent."""
    if inp.shape != expected.shape or np.array_equal(inp, expected):
        return False
    diff = inp != expected
    return bool(np.all(inp[diff] == 0))


def _detect_symmetrize(inp: Grid, expected: Grid) -> bool:
    """expected est symétrique (H, V ou 180°) alors que l'input ne l'est pas."""
    if inp.shape != expected.shape:
        return False

    def symmetric(g: Grid) -> bool:
        return (
            np.array_equal(g, np.flipud(g))
            or np.array_equal(g, np.fliplr(g))
            or np.array_equal(g, np.rot90(g, 2))
        )

    return symmetric(expected) and not symmetric(inp)


def _detect_count_reduce(inp: Grid, expected: Grid) -> bool:
    """Réduction forte : la sortie est minuscule devant l'entrée (comptage)."""
    return expected.size <= 4 and inp.size >= 4 * expected.size


def _detect_select_subgrid(inp: Grid, expected: Grid) -> bool:
    """expected apparaît telle quelle comme sous-grille de l'input."""
    ih, iw = inp.shape
    eh, ew = expected.shape
    if eh > ih or ew > iw or (eh == ih and ew == iw):
        return False
    for i in range(ih - eh + 1):
        for j in range(iw - ew + 1):
            if np.array_equal(inp[i : i + eh, j : j + ew], expected):
                return True
    return False


# (nom de primitive, catégorie principalement débloquée, détecteur)
PRIMITIVE_DETECTORS: list[tuple[str, str, Callable[[Grid, Grid], bool]]] = [
    ("recolor_map (table de couleurs complète)", "wrong_colors", _detect_recolor_map),
    ("extract_object (segmentation en objets)", "wrong_size", _detect_extract_object),
    ("select_block (partition régulière)", "wrong_size", _detect_select_block),
    ("tile_with_flips (pavage ∘ symétries)", "wrong_size", _detect_tile_transform),
    ("fill_background (remplissage du fond)", "structure_missed", _detect_fill_background),
    ("symmetrize (complétion de symétrie)", "structure_missed", _detect_symmetrize),
    ("count_reduce (comptage / réduction)", "wrong_size", _detect_count_reduce),
    ("select_subgrid (sélection de sous-grille)", "wrong_size", _detect_select_subgrid),
]


def recommend_primitives(
    task_ids: set[str], tasks: dict[str, Task]
) -> list[tuple[str, str, int]]:
    """[(primitive, catégorie débloquée, nb de tâches expliquées)], décroissant."""
    counts: Counter[str] = Counter()
    category_of = {name: cat for name, cat, _fn in PRIMITIVE_DETECTORS}
    for tid in task_ids:
        task = tasks.get(tid)
        if task is None:
            continue
        test_in, expected = task.test_pairs[0]
        for name, _cat, fn in PRIMITIVE_DETECTORS:
            if fn(test_in, expected):
                counts[name] += 1
    ranked = [(name, category_of[name], n) for name, n in counts.most_common()]
    return ranked[:10]


# --- rapport ----------------------------------------------------------------


def _comment(task: Task, r: dict[str, Any]) -> str:
    test_in, expected = task.test_pairs[0]
    produced = _first_attempt(r["meta"])
    if produced is None:
        return f"aucune sortie exploitable (statut {r['status']})"
    produced_arr = np.asarray(produced)
    if produced_arr.shape != expected.shape:
        return (
            f"forme produite {produced_arr.shape} ≠ attendue {expected.shape} "
            f"(input {test_in.shape})"
        )
    hamming = float(np.mean(produced_arr != expected))
    return f"forme correcte, {hamming:.1%} de cellules fausses"


def taxonomy_report(
    run_ids: tuple[str, ...] = OFFICIAL_RUNS,
    db_path: Path | str | None = None,
    out_dir: Path | str | None = None,
) -> Path:
    db = sqlite3.connect(str(db_path or DEFAULT_DB_PATH))
    results = {rid: _fetch_results(db, rid) for rid in run_ids}
    db.close()

    all_failed_ids = sorted(
        {tid for res in results.values() for tid, r in res.items() if r["status"] != "solved"}
    )
    tasks = _load_tasks_by_id(all_failed_ids)
    labels = {rid: categorize_run(res, tasks) for rid, res in results.items()}

    lines = [
        "# Taxonomie des échecs EPIC-0 (X-60)",
        "",
        f"Runs analysés : {', '.join(f'`{r}`' for r in run_ids)} — "
        f"seuil near_miss < {NEAR_MISS_THRESHOLD:.0%} de cellules fausses.",
        "",
        "## Masses par catégorie",
        "",
        "| catégorie | " + " | ".join(run_ids) + " |",
        "|---|" + "---|" * len(run_ids),
    ]
    for cat in CATEGORIES:
        row = [str(sum(1 for c in labels[rid].values() if c == cat)) for rid in run_ids]
        lines.append(f"| {cat} | " + " | ".join(row) + " |")

    # -- croisement des runs --------------------------------------------------
    failed_sets = {rid: set(lbl) for rid, lbl in labels.items()}
    common = set.intersection(*failed_sets.values()) if failed_sets else set()
    lines += ["", "## Croisement des runs", ""]
    lines.append(f"- Échecs communs aux {len(run_ids)} solveurs : **{len(common)}**")
    for rid in run_ids:
        others = [s for r, s in failed_sets.items() if r != rid]
        only = failed_sets[rid].difference(*others) if others else failed_sets[rid]
        lines.append(f"- Échecs propres à `{rid}` : {len(only)}")

    # -- 3 exemples commentés par catégorie -----------------------------------
    # On privilégie le run le plus fort (dernier de la liste) pour les exemples.
    ref_run = run_ids[-1]
    lines += ["", "## Exemples par catégorie (run de référence : " + f"`{ref_run}`)"]
    for cat in CATEGORIES:
        examples = [tid for tid, c in sorted(labels[ref_run].items()) if c == cat]
        if not examples:  # repli sur les autres runs
            for rid in run_ids:
                examples = [tid for tid, c in sorted(labels[rid].items()) if c == cat]
                if examples:
                    ref = rid
                    break
            else:
                ref = ref_run
        else:
            ref = ref_run
        lines += ["", f"### {cat}", ""]
        if not examples:
            lines.append("Aucune tâche dans cette catégorie.")
            continue
        for tid in examples[:3]:
            if tid in tasks:
                comment = _comment(tasks[tid], results[ref][tid])
            else:
                comment = "tâche absente du dataset local"
            lines.append(f"- `{tid}` ({ref}) — {comment}")

    # -- recommandation de primitives -----------------------------------------
    ranked = recommend_primitives(common, tasks)
    lines += [
        "",
        "## Primitives DSL v1 candidates (≤ 10)",
        "",
        f"Comptées sur les {len(common)} échecs communs aux {len(run_ids)} solveurs "
        "— une tâche peut être expliquée par plusieurs primitives.",
        "",
        "| primitive candidate | catégorie débloquée | tâches expliquées |",
        "|---|---|---|",
    ]
    if not ranked:
        lines.append("| (aucun détecteur ne matche) | — | 0 |")
    for name, cat, n in ranked:
        lines.append(f"| {name} | {cat} | {n} |")

    out_dir = Path(out_dir or REPORTS_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "taxonomy_epic0.md"
    out_path.write_text("\n".join(lines) + "\n")
    return out_path
