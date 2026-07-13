"""X-51 — critères d'acceptation du loader et des splits scellés."""

from __future__ import annotations

import json

import pytest

from solveur.data.loader import (
    SPLIT_SEED,
    SPLITS_PATH,
    FinalSetLockedError,
    Task,
    generate_splits,
    get_split,
    load_all_tasks,
    load_splits,
)


@pytest.fixture(scope="session")
def all_tasks() -> dict[str, Task]:
    return load_all_tasks()


def test_load_all_tasks(all_tasks: dict[str, Task]) -> None:
    assert len(all_tasks) > 1500  # 800 arc1 + ~1120 arc2
    for task in all_tasks.values():
        assert task.train_pairs and task.test_pairs
        for grid_in, grid_out in task.train_pairs + task.test_pairs:
            for grid in (grid_in, grid_out):
                assert grid.dtype.name == "int8"
                assert 1 <= grid.shape[0] <= 30 and 1 <= grid.shape[1] <= 30
                assert grid.min() >= 0 and grid.max() <= 9


def test_splits_disjoint() -> None:
    splits = load_splits()["splits"]
    dev, val, final = (set(splits[k]) for k in ("dev", "validation", "final"))
    assert not dev & val and not dev & final and not val & final


def test_splits_stable(all_tasks: dict[str, Task]) -> None:
    regenerated = generate_splits(all_tasks, seed=SPLIT_SEED)
    assert regenerated == json.loads(SPLITS_PATH.read_text())


def test_splits_counts() -> None:
    counts = load_splits()["counts"]
    assert counts["dev"] == 200
    assert counts["validation"] == 160


def test_final_locked(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FINAL_RUN", raising=False)
    with pytest.raises(FinalSetLockedError):
        get_split("final")


def test_dev_split_loads() -> None:
    dev = get_split("dev")
    assert len(dev) == 200
    assert all(t.source == "arc1/training" for t in dev)
