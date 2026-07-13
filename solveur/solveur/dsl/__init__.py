"""X-55 — DSL minimale (10 primitives) et recherche brute-force."""

from solveur.dsl.core import (
    PRIMITIVE_FACTORIES,
    Program,
    enumerate_programs,
    instantiate_primitives,
    run_program,
    search,
)

__all__ = [
    "PRIMITIVE_FACTORIES",
    "Program",
    "enumerate_programs",
    "instantiate_primitives",
    "run_program",
    "search",
]
