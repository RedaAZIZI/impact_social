"""Grammaire textuelle de la DSL et parseur (X-63).

Syntaxe : une composition = primitives séparées par `|`, appliquées de gauche
à droite. Exemple : `recolor(2->0) | fill_enclosed(3)`. Une ligne = un
programme candidat. C'est le format que le proposeur LLM (T-1.3b) doit
produire et que le vérifieur exécute via `run_program` — la référence de la
grammaire donnée au prompt est générée depuis le code (`dsl_reference`) pour
ne jamais diverger de l'interpréteur.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from solveur.dsl.core import (
    PRIMITIVE_FACTORIES as _FACTORIES,
)
from solveur.dsl.core import (
    Primitive,
    Program,
    fill_enclosed,
    fill_holes_per_object,
    recolor,
    scale,
    tile,
)

COLOR_DOMAIN = range(10)  # couleurs ARC : 0-9


class DSLParseError(ValueError):
    """Programme DSL invalide ; le message dit quoi et pourquoi."""


# (signature, sémantique une ligne, domaine des arguments)
_SPECS: dict[str, tuple[str, str]] = {
    "rotate90": ("rotate90", "rotation de 90° anti-horaire"),
    "rotate180": ("rotate180", "rotation de 180°"),
    "flip_h": ("flip_h", "miroir horizontal (gauche-droite)"),
    "flip_v": ("flip_v", "miroir vertical (haut-bas)"),
    "transpose": ("transpose", "transposition lignes/colonnes"),
    "crop_to_content": (
        "crop_to_content",
        "rogne au plus petit rectangle contenant les cellules non nulles",
    ),
    "identity": ("identity", "grille inchangée"),
    "recolor": ("recolor(a->b)", "remplace la couleur a par b (a, b dans 0-9)"),
    "tile": ("tile(nx,ny)", "pave la grille nx fois en largeur, ny en hauteur"),
    "scale": ("scale(k)", "agrandit chaque cellule en bloc k×k"),
    "fill_enclosed": (
        "fill_enclosed(c)",
        "colorie en c les régions de fond (0) ne touchant pas le bord",
    ),
    "fill_holes_per_object": (
        "fill_holes_per_object(c)",
        "colorie en c les trous de fond enclos dans la bbox de chaque objet",
    ),
}

_CALL_RE = re.compile(r"^(?P<name>[a-z_0-9]+)(?:\((?P<args>[^()]*)\))?$")


def _parse_color(raw: str, call: str) -> int:
    try:
        value = int(raw)
    except ValueError:
        raise DSLParseError(f"`{call}` : argument `{raw}` n'est pas un entier") from None
    if value not in COLOR_DOMAIN:
        raise DSLParseError(f"`{call}` : couleur {value} hors domaine 0-9")
    return value


def _parse_positive(raw: str, call: str) -> int:
    try:
        value = int(raw)
    except ValueError:
        raise DSLParseError(f"`{call}` : argument `{raw}` n'est pas un entier") from None
    if not 1 <= value <= 30:
        raise DSLParseError(f"`{call}` : paramètre {value} hors domaine 1-30")
    return value


def parse_call(text: str) -> tuple[str, Primitive]:
    """`recolor(2->0)` -> (nom canonique, primitive exécutable)."""
    call = text.strip()
    m = _CALL_RE.match(call)
    if not m:
        raise DSLParseError(f"`{call}` : syntaxe invalide (attendu `nom` ou `nom(args)`)")
    name, args = m.group("name"), m.group("args")
    if name not in _FACTORIES:
        known = ", ".join(sorted(_FACTORIES))
        raise DSLParseError(f"`{call}` : primitive inconnue (connues : {known})")

    if name in ("rotate90", "rotate180", "flip_h", "flip_v", "transpose",
                "crop_to_content", "identity"):
        if args:
            raise DSLParseError(f"`{call}` : {name} ne prend pas d'argument")
        return name, _FACTORIES[name]  # type: ignore[return-value]

    if args is None:
        raise DSLParseError(f"`{call}` : {name} exige des arguments ({_SPECS[name][0]})")

    if name == "recolor":
        parts = args.split("->")
        if len(parts) != 2:
            raise DSLParseError(f"`{call}` : recolor attend `a->b`")
        a, b = (_parse_color(p.strip(), call) for p in parts)
        if a == b:
            raise DSLParseError(f"`{call}` : recolor exige a ≠ b")
        return f"recolor({a}->{b})", recolor(a, b)
    if name == "tile":
        parts = [p.strip() for p in args.split(",")]
        if len(parts) != 2:
            raise DSLParseError(f"`{call}` : tile attend `nx,ny`")
        nx, ny = (_parse_positive(p, call) for p in parts)
        return f"tile({nx},{ny})", tile(nx, ny)
    if name == "scale":
        k = _parse_positive(args.strip(), call)
        return f"scale({k})", scale(k)
    if name == "fill_enclosed":
        c = _parse_color(args.strip(), call)
        return f"fill_enclosed({c})", fill_enclosed(c)
    # fill_holes_per_object
    c = _parse_color(args.strip(), call)
    return f"fill_holes_per_object({c})", fill_holes_per_object(c)


def parse_program(text: str) -> tuple[Program, dict[str, Primitive]]:
    """Parse une composition `p1 | p2 | ...` (gauche → droite).

    Retourne (programme au format de `run_program`, primitives exécutables).
    Tolère backticks, puces et espaces ; lève DSLParseError sinon.
    """
    cleaned = text.strip().strip("`").strip()
    cleaned = re.sub(r"^[-*\d.\s]+", "", cleaned).strip()
    if not cleaned:
        raise DSLParseError("programme vide")
    names: list[str] = []
    prims: dict[str, Primitive] = {}
    for part in cleaned.split("|"):
        name, prim = parse_call(part)
        names.append(name)
        prims[name] = prim
    return tuple(names), prims


def serialize_program(program: Program) -> str:
    """Programme -> texte (inverse de parse_program sur les noms canoniques)."""
    return " | ".join(program)


@dataclass
class ExtractionResult:
    programs: list[tuple[Program, dict[str, Primitive]]]
    rejected: list[tuple[str, str]]  # (ligne, raison)


def extract_programs(llm_text: str, k: int | None = None) -> ExtractionResult:
    """Extrait les programmes d'une réponse LLM ; ne lève jamais.

    Cherche les blocs ``` (avec ou sans tag `dsl`) ; à défaut, lit toutes les
    lignes. Retourne au plus k programmes valides, plus les rejets motivés.
    """
    blocks = re.findall(r"```(?:dsl)?\s*\n(.*?)```", llm_text, flags=re.DOTALL)
    source = "\n".join(blocks) if blocks else llm_text
    valid: list[tuple[Program, dict[str, Primitive]]] = []
    seen: set[Program] = set()
    rejected: list[tuple[str, str]] = []
    for line in source.splitlines():
        if not line.strip():
            continue
        if k is not None and len(valid) >= k:
            break
        try:
            program, prims = parse_program(line)
        except DSLParseError as e:
            rejected.append((line.strip(), str(e)))
            continue
        if program in seen:
            continue
        seen.add(program)
        valid.append((program, prims))
    return ExtractionResult(programs=valid, rejected=rejected)


def dsl_reference() -> str:
    """Documentation de la grammaire pour le prompt du proposeur.

    Générée depuis le code : chaque primitive de PRIMITIVE_FACTORIES y figure.
    """
    lines = [
        "Un programme = primitives séparées par `|`, appliquées de gauche à droite.",
        "Exemple : `recolor(2->0) | fill_enclosed(3)`. Une ligne = un programme.",
        "",
        "Primitives disponibles :",
    ]
    for name in sorted(_FACTORIES):
        signature, doc = _SPECS[name]
        lines.append(f"- `{signature}` : {doc}")
    return "\n".join(lines)
