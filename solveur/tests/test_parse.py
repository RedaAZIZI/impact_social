"""X-63 — critères d'acceptation de la grammaire DSL et du parseur."""

from __future__ import annotations

import numpy as np
import pytest

from solveur.data.loader import Task
from solveur.dsl.core import PRIMITIVE_FACTORIES, instantiate_primitives, run_program, search
from solveur.dsl.parse import (
    DSLParseError,
    dsl_reference,
    extract_programs,
    parse_program,
    serialize_program,
)

G = lambda rows: np.array(rows, dtype=np.int8)  # noqa: E731


class TestParseProgram:
    def test_simple_and_composition(self) -> None:
        program, _ = parse_program("rotate90")
        assert program == ("rotate90",)
        program, _ = parse_program("recolor(2->0) | fill_enclosed(3)")
        assert program == ("recolor(2->0)", "fill_enclosed(3)")

    def test_noise_tolerance(self) -> None:
        for text in ("`rotate90`", "- rotate90", "1. rotate90", "  rotate90  "):
            assert parse_program(text)[0] == ("rotate90",)

    @pytest.mark.parametrize(
        ("text", "fragment"),
        [
            ("", "vide"),
            ("frobnicate", "primitive inconnue"),
            ("rotate90(3)", "ne prend pas d'argument"),
            ("recolor(2)", "attend `a->b`"),
            ("recolor(2->2)", "a ≠ b"),
            ("recolor(12->0)", "hors domaine 0-9"),
            ("fill_enclosed(x)", "n'est pas un entier"),
            ("fill_enclosed(11)", "hors domaine 0-9"),
            ("scale(0)", "hors domaine 1-30"),
            ("tile(2)", "attend `nx,ny`"),
            ("scale", "exige des arguments"),
        ],
    )
    def test_rejects(self, text: str, fragment: str) -> None:
        with pytest.raises(DSLParseError, match=".*"):
            try:
                parse_program(text)
            except DSLParseError as e:
                assert fragment in str(e)
                raise

    def test_execution_matches_interpreter(self) -> None:
        # un programme parsé s'exécute via run_program, y compris avec une
        # couleur absente des sorties train (choix libre du LLM)
        program, prims = parse_program("fill_enclosed(7)")
        grid = G([[2, 2, 2], [2, 0, 2], [2, 2, 2]])
        out = run_program(program, prims, grid)
        assert out is not None and out[1, 1] == 7


def make_task(train, test):  # type: ignore[no-untyped-def]
    return Task(
        task_id="mock/parse",
        source="mock",
        train_pairs=[(G(a), G(b)) for a, b in train],
        test_pairs=[(G(a), G(b)) for a, b in test],
    )


def test_round_trip_brute_force_programs() -> None:
    # tout programme trouvé par le brute-force se sérialise puis se reparse identique
    tasks = [
        make_task(train=[([[1, 2], [3, 4]], [[4, 3], [2, 1]])], test=[([[1]], [[1]])]),
        make_task(
            train=[
                ([[2, 2, 2], [2, 0, 2], [2, 2, 2]], [[2, 2, 2], [2, 4, 2], [2, 2, 2]]),
                (
                    [[2, 2, 2, 0], [2, 0, 2, 0], [2, 2, 2, 0]],
                    [[2, 2, 2, 0], [2, 4, 2, 0], [2, 2, 2, 0]],
                ),
            ],
            test=[([[1]], [[1]])],
        ),
    ]
    for task in tasks:
        result = search(task)
        assert result.program is not None
        reparsed, prims = parse_program(serialize_program(result.program))
        assert reparsed == result.program
        # même sortie via les primitives reparsées et celles de la tâche
        grid = task.train_pairs[0][0]
        expected = run_program(result.program, instantiate_primitives(task), grid)
        assert np.array_equal(run_program(reparsed, prims, grid), expected)


def test_extract_programs_from_noisy_llm_answer() -> None:
    answer = """Je vois une symétrie. Voici mes candidats :

```dsl
rotate90
recolor(2->0) | fill_enclosed(3)
frobnicate(1)
recolor(2->0) | fill_enclosed(3)
fill_enclosed(12)
```

En dehors du bloc : scale(2) — à ignorer.
"""
    result = extract_programs(answer, k=4)
    assert [p for p, _ in result.programs] == [
        ("rotate90",),
        ("recolor(2->0)", "fill_enclosed(3)"),
    ]  # doublon dédupliqué, invalides rejetés, hors-bloc ignoré
    reasons = dict(result.rejected)
    assert "frobnicate(1)" in reasons and "fill_enclosed(12)" in reasons


def test_extract_programs_without_block_and_k_cap() -> None:
    result = extract_programs("rotate90\nflip_h\nflip_v", k=2)
    assert len(result.programs) == 2


def test_extract_programs_never_raises() -> None:
    assert extract_programs("").programs == []
    assert extract_programs("du texte sans aucun programme").programs == []


def test_dsl_reference_covers_all_primitives() -> None:
    ref = dsl_reference()
    for name in PRIMITIVE_FACTORIES:
        assert name in ref
