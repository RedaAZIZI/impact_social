"""Loader ARC-AGI-1/2 : téléchargement, parsing, splits scellés (X-51).

Splits générés UNE SEULE FOIS avec SPLIT_SEED puis scellés dans splits.json
(committé). Le split "final" est verrouillé : y accéder sans FINAL_RUN=1 lève
FinalSetLockedError. Ce verrou ne se contourne jamais (CLAUDE.md, règle 3).
"""

from __future__ import annotations

import concurrent.futures
import json
import os
import random
import time
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

Grid = np.ndarray

# Seed documenté des splits scellés — ne jamais changer sans décision de Reda.
SPLIT_SEED = 20260713

PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parents[1]  # dossier solveur/ (racine projet)
RAW_DIR = PROJECT_ROOT / "data" / "raw"
SPLITS_PATH = PACKAGE_DIR / "splits.json"
MANIFEST_PATH = PACKAGE_DIR / "manifest.json"

# Contenu téléchargé fichier par fichier depuis les repos OFFICIELS.
# (manifest.json committé liste les task_ids ; certains environnements
# bloquent les archives zip de github.com mais pas raw.githubusercontent.com)
RAW_BASE_URLS = {
    "arc1": "https://raw.githubusercontent.com/fchollet/ARC-AGI/master/data",
    "arc2": "https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/data",
}


class FinalSetLockedError(RuntimeError):
    """Le split final est scellé : accès refusé sans FINAL_RUN=1."""


@dataclass
class Task:
    task_id: str  # ex. "arc1/training/007bbfb7"
    source: str  # "arc1/training", "arc1/evaluation", "arc2/training", "arc2/evaluation"
    train_pairs: list[tuple[Grid, Grid]] = field(default_factory=list)
    test_pairs: list[tuple[Grid, Grid]] = field(default_factory=list)


def _to_grid(cells: list[list[int]]) -> Grid:
    grid = np.array(cells, dtype=np.int8)
    if grid.ndim != 2:
        raise ValueError(f"grille non 2D : shape={grid.shape}")
    return grid


def _parse_task(task_id: str, source: str, raw: dict) -> Task:
    return Task(
        task_id=task_id,
        source=source,
        train_pairs=[(_to_grid(p["input"]), _to_grid(p["output"])) for p in raw["train"]],
        test_pairs=[(_to_grid(p["input"]), _to_grid(p["output"])) for p in raw["test"]],
    )


def _fetch_one(url: str, dest: Path, retries: int = 5) -> None:
    delay = 1.0
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                payload = resp.read()
            json.loads(payload)  # refuse tout contenu non-JSON (page d'erreur, proxy)
            dest.write_bytes(payload)
            return
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(delay)
            delay *= 2


def download_datasets(raw_dir: Path | None = None, force: bool = False) -> Path:
    """Télécharge les tâches manquantes depuis les repos officiels (par fichier)."""
    raw_dir = raw_dir or RAW_DIR
    manifest = json.loads(MANIFEST_PATH.read_text())
    jobs: list[tuple[str, Path]] = []
    for source, subdirs in manifest.items():
        for split_name, task_ids in subdirs.items():
            out_dir = raw_dir / source / split_name
            out_dir.mkdir(parents=True, exist_ok=True)
            for task_id in task_ids:
                dest = out_dir / f"{task_id}.json"
                if force or not dest.exists():
                    jobs.append((f"{RAW_BASE_URLS[source]}/{split_name}/{task_id}.json", dest))
    if jobs:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda j: _fetch_one(*j), jobs))
    return raw_dir


def load_all_tasks(raw_dir: Path | None = None) -> dict[str, Task]:
    """Charge toutes les tâches des deux datasets (téléchargées si absentes)."""
    raw_dir = download_datasets(raw_dir)
    manifest = json.loads(MANIFEST_PATH.read_text())
    tasks: dict[str, Task] = {}
    for source, subdirs in manifest.items():
        for split_name in subdirs:
            for path in sorted((raw_dir / source / split_name).glob("*.json")):
                src = f"{source}/{split_name}"
                task_id = f"{src}/{path.stem}"
                tasks[task_id] = _parse_task(task_id, src, json.loads(path.read_text()))
    if not tasks:
        raise RuntimeError(f"aucune tâche trouvée dans {raw_dir}")
    return tasks


def generate_splits(tasks: dict[str, Task], seed: int = SPLIT_SEED) -> dict:
    """Génère les splits scellés. Déterministe pour un seed donné.

    dev        : 200 tâches arc1/training
    validation : 100 tâches arc1/evaluation + 60 tâches arc2 (evaluation)
    final      : tout le reste
    """
    rng = random.Random(seed)
    arc1_train = sorted(t for t in tasks if t.startswith("arc1/training/"))
    arc1_eval = sorted(t for t in tasks if t.startswith("arc1/evaluation/"))
    arc2_eval = sorted(t for t in tasks if t.startswith("arc2/evaluation/"))

    dev = sorted(rng.sample(arc1_train, 200))
    validation = sorted(rng.sample(arc1_eval, 100) + rng.sample(arc2_eval, 60))
    reserved = set(dev) | set(validation)
    final = sorted(t for t in tasks if t not in reserved)

    return {
        "seed": seed,
        "counts": {"dev": len(dev), "validation": len(validation), "final": len(final)},
        "splits": {"dev": dev, "validation": validation, "final": final},
    }


def load_splits() -> dict:
    return json.loads(SPLITS_PATH.read_text())


def get_split(name: str, raw_dir: Path | None = None) -> list[Task]:
    """Retourne les tâches d'un split. Le split final est verrouillé."""
    if name == "final" and os.environ.get("FINAL_RUN") != "1":
        raise FinalSetLockedError(
            "Le split final est scellé. Il ne peut être chargé qu'avec FINAL_RUN=1, "
            "posé par un humain pour le run final officiel."
        )
    splits = load_splits()["splits"]
    if name not in splits:
        raise KeyError(f"split inconnu : {name!r} (attendu : {sorted(splits)})")
    tasks = load_all_tasks(raw_dir)
    return [tasks[task_id] for task_id in splits[name]]
