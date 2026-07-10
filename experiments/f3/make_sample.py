# -*- coding: utf-8 -*-
"""F3 campagne 1 — tirage de l'échantillon d'annotation humaine.

Pré-enregistrement : docs/PREREGISTREMENT_F3.md (gelé AVANT ouverture des
données, commit af2ecd6). Seed unique : 20260706. Tirage déterministe, pas de
re-tirage.

Strates (300 clauses) :
  - e-SNLI (explicatif)          : 100  (30 prédites A par le classifieur + 70 autres)
  - LIAR-PLUS (calibration)      : 100  (30 A + 70 autres)
  - based.cooking ingrédients    :  50  (15 A + 35 autres)
  - based.cooking étapes         :  50  (15 A + 35 autres)

L'unité est la CLAUSE (guide §1) : les phrases sont segmentées par une règle
déterministe (voir split_clauses) AVANT tirage ; le classifieur est appliqué
au niveau clause pour constituer le vivier A. L'échantillon sert à mesurer
l'accord inter-juges et à valider l'instrument — PAS à estimer des taux
(sur-représentation délibérée de A).

Sorties :
  - sample_annotation.csv : feuille en AVEUGLE (id, clause, colonnes vides)
  - sample_key.csv        : clé (strate, origine, étiquettes classifieur) —
                            à ne pas montrer aux juges avant adjudication.
"""
import csv, glob, json, math, random, re, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pilote_f3"))
from i1_classifier import classify  # noqa: E402

SEED = 20260706
PILOTE = os.path.join(os.path.dirname(__file__), "..", "pilote_f3")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

# Règle déterministe de segmentation en clauses (guide §1 : conjonctions et
# relatives). On coupe sur ces jonctions si chaque côté garde >= 3 mots.
CLAUSE_SPLIT = re.compile(
    r";\s+|,\s+(?=(?:and|but|so|because|while|whereas|although|which|who)\b)"
    r"|\s+(?=(?:because|although|whereas|while)\b)")


def split_clauses(sentence):
    parts = [p.strip(" ,;") for p in CLAUSE_SPLIT.split(sentence)]
    parts = [p for p in parts if p]
    out, buf = [], ""
    for p in parts:
        buf = (buf + " " + p).strip() if buf else p
        if len(buf.split()) >= 3:
            out.append(buf)
            buf = ""
    if buf:  # reliquat court : rattaché à la dernière clause
        if out:
            out[-1] = out[-1] + " " + buf
        else:
            out = [buf]
    return out


def load_esnli():
    sents = []
    for fn in ["esnli_dev.csv", "esnli_test.csv"]:
        with open(os.path.join(PILOTE, "data", fn), encoding="utf-8") as f:
            for row in csv.DictReader(f):
                e = (row.get("Explanation_1") or "").strip()
                if len(e.split()) >= 3:
                    sents.append(e)
    return sents


def load_liar():
    sents = []
    for fn in ["liar_val2.tsv", "liar_test2.tsv"]:
        with open(os.path.join(PILOTE, "data", fn), encoding="utf-8") as f:
            for line in f:
                cols = line.rstrip("\n").split("\t")
                if len(cols) < 16:
                    continue
                just = cols[15].strip()
                if not just or just.lower() == "nan":
                    continue
                sents.extend(s.strip() for s in SENT_SPLIT.split(just)
                             if len(s.split()) >= 4)
    return sents


def load_recettes():
    ing, steps = [], []
    for fn in sorted(glob.glob(os.path.join(PILOTE, "recettes/content/*.md"))):
        if fn.endswith("_index.md"):
            continue
        sec = None
        for line in open(fn, encoding="utf-8").read().splitlines():
            l = line.strip()
            if l.lower().startswith("## ingredient"):
                sec = "ing"; continue
            if l.lower().startswith("## direction"):
                sec = "dir"; continue
            if l.startswith("##"):
                sec = None; continue
            if not l or sec is None:
                continue
            l = re.sub(r"^[-*]\s+|^\d+[.)]\s+", "", l)
            if len(l.split()) < 2:
                continue
            if sec == "ing":
                ing.append(l)
            else:
                steps.extend(s for s in SENT_SPLIT.split(l)
                             if len(s.split()) >= 3)
    return ing, steps


def draw(clauses, n_a, n_rest, rng):
    """Tire n_a clauses prédites A + n_rest parmi le reste (sans remise)."""
    tagged = [(c, classify(c)) for c in clauses]
    pool_a = sorted({c for c, r in tagged if r["tags"]["A"]})
    pool_rest = sorted({c for c, r in tagged if not r["tags"]["A"]})
    take_a = pool_a if len(pool_a) <= n_a else rng.sample(pool_a, n_a)
    short = n_a - len(take_a)  # vivier A insuffisant -> complété par le reste
    take_r = rng.sample(pool_rest, n_rest + short)
    return [(c, classify(c)) for c in take_a + take_r]


def main():
    rng = random.Random(SEED)
    esnli = [c for s in load_esnli() for c in split_clauses(s)]
    liar = [c for s in load_liar() for c in split_clauses(s)]
    ing_raw, steps_raw = load_recettes()
    ing = [c for s in ing_raw for c in split_clauses(s)]
    steps = [c for s in steps_raw for c in split_clauses(s)]

    strata = [
        ("esnli", draw(esnli, 30, 70, rng)),
        ("liar", draw(liar, 30, 70, rng)),
        ("recettes-ingredients", draw(ing, 15, 35, rng)),
        ("recettes-etapes", draw(steps, 15, 35, rng)),
    ]
    units = [(name, c, r) for name, items in strata for c, r in items]
    rng.shuffle(units)

    here = os.path.dirname(__file__) or "."
    with open(os.path.join(here, "sample_annotation.csv"), "w",
              encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "clause", "etiquettes (parmi A,I,C,N,OTHER — "
                    "multi autorisé, ex. \"I,C\")", "commentaire"])
        for i, (_, c, _) in enumerate(units, 1):
            w.writerow([f"F3-{i:03d}", c, "", ""])

    with open(os.path.join(here, "sample_key.csv"), "w",
              encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "strate", "clf_tags", "clf_excl", "clf_sub"])
        for i, (name, c, r) in enumerate(units, 1):
            tags = ",".join(k for k in ["A", "I", "C", "N"] if r["tags"][k]) \
                   or "OTHER"
            w.writerow([f"F3-{i:03d}", name, tags, r["excl"],
                        ";".join(r["sub"])])

    n_a = sum(1 for _, _, r in units if r["tags"]["A"])
    print(f"{len(units)} clauses tirées (seed {SEED}), "
          f"dont {n_a} prédites A par le classifieur.")
    for name, items in strata:
        print(f"  {name}: {len(items)}")


if __name__ == "__main__":
    main()
