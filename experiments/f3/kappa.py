# -*- coding: utf-8 -*-
"""F3 campagne 1 — accord inter-juges et validation de l'instrument.

Mesures pré-enregistrées (docs/PREREGISTREMENT_F3.md §5) :
  - κ de Cohen par classe (binaire classe-vs-reste) + κ global sur la classe
    exclusive (priorité A > I > C > N > OTHER) ;
  - IC 95 % par bootstrap (10 000 rééchantillonnages, seed 20260706) ;
  - si un or adjudiqué est fourni : précision/rappel du classifieur par
    classe contre l'or (IC de Wilson) — verdict H-V.

Verdict H-κ : κ(A) >= 0,7.

Usage :
  python3 kappa.py juge1.csv juge2.csv [--gold gold.csv]

Format attendu des feuilles remplies : celui de sample_annotation.csv, la
3e colonne contenant les étiquettes (ex. "I,C" ; vide = OTHER). Le fichier
gold (or adjudiqué) suit le même format.
"""
import csv, math, random, sys, os

SEED = 20260706
CLASSES = ["A", "I", "C", "N", "OTHER"]
PRIORITY = ["A", "I", "C", "N", "OTHER"]
KAPPA_A_TARGET = 0.7


def read_sheet(path):
    labels = {}
    with open(path, encoding="utf-8") as f:
        rows = list(csv.reader(f))
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        tags = {t.strip().upper() for t in (row[2] if len(row) > 2 else "")
                .replace(";", ",").split(",") if t.strip()}
        bad = tags - set(CLASSES)
        if bad:
            sys.exit(f"{path}: étiquette inconnue {bad} sur {row[0]}")
        labels[row[0].strip()] = tags or {"OTHER"}
    return labels


def exclusive(tags):
    for c in PRIORITY:
        if c in tags:
            return c
    return "OTHER"


def cohen_kappa(pairs):
    """pairs : liste de (label1, label2) catégoriels."""
    n = len(pairs)
    if n == 0:
        return float("nan")
    cats = sorted({a for a, _ in pairs} | {b for _, b in pairs})
    po = sum(1 for a, b in pairs if a == b) / n
    pe = sum((sum(1 for a, _ in pairs if a == c) / n)
             * (sum(1 for _, b in pairs if b == c) / n) for c in cats)
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1 - pe)


def bootstrap_ci(pairs, stat, n_boot=10_000, seed=SEED):
    rng = random.Random(seed)
    n = len(pairs)
    vals = []
    for _ in range(n_boot):
        sample = [pairs[rng.randrange(n)] for _ in range(n)]
        v = stat(sample)
        if not math.isnan(v):
            vals.append(v)
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))]


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"),) * 3
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def main():
    argv = sys.argv[1:]
    gold_path = None
    if "--gold" in argv:
        i = argv.index("--gold")
        gold_path = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    args = argv
    if len(args) != 2:
        sys.exit(__doc__)

    j1, j2 = read_sheet(args[0]), read_sheet(args[1])
    ids = sorted(set(j1) & set(j2))
    missing = (set(j1) | set(j2)) - set(ids)
    if missing:
        print(f"⚠ {len(missing)} unités absentes d'une des feuilles — exclues")
    print(f"n = {len(ids)} clauses annotées par les deux juges\n")

    print("κ de Cohen, binaire classe-vs-reste (IC 95 % bootstrap) :")
    kappa_a = None
    for c in CLASSES:
        pairs = [(c in j1[i], c in j2[i]) for i in ids]
        k = cohen_kappa(pairs)
        lo, hi = bootstrap_ci(pairs, cohen_kappa)
        if c == "A":
            kappa_a = k
        print(f"  {c:5s}: κ = {k:.3f}  [{lo:.3f}–{hi:.3f}]")

    pairs_excl = [(exclusive(j1[i]), exclusive(j2[i])) for i in ids]
    kg = cohen_kappa(pairs_excl)
    lo, hi = bootstrap_ci(pairs_excl, cohen_kappa)
    print(f"  global (classe exclusive) : κ = {kg:.3f}  [{lo:.3f}–{hi:.3f}]")

    verdict = "POSITIF" if kappa_a >= KAPPA_A_TARGET else "NÉGATIF"
    print(f"\nVerdict H-κ (κ(A) >= {KAPPA_A_TARGET}) : {verdict} "
          f"(κ(A) = {kappa_a:.3f})")

    if gold_path:
        here = os.path.dirname(os.path.abspath(__file__))
        key = {}
        with open(os.path.join(here, "sample_key.csv"), encoding="utf-8") as f:
            for row in csv.DictReader(f):
                key[row["id"]] = {t for t in row["clf_tags"].split(",") if t}
        gold = read_sheet(gold_path)
        gids = sorted(set(gold) & set(key))
        print(f"\nValidation de l'instrument contre l'or adjudiqué "
              f"(n = {len(gids)}) :")
        for c in CLASSES:
            tp = sum(1 for i in gids if c in key[i] and c in gold[i])
            fp = sum(1 for i in gids if c in key[i] and c not in gold[i])
            fn = sum(1 for i in gids if c not in key[i] and c in gold[i])
            p, plo, phi = wilson(tp, tp + fp)
            r, rlo, rhi = wilson(tp, tp + fn)
            print(f"  {c:5s}: précision = {p:.2f} [{plo:.2f}–{phi:.2f}]  "
                  f"rappel = {r:.2f} [{rlo:.2f}–{rhi:.2f}]  "
                  f"(tp={tp} fp={fp} fn={fn})")
        # verdict H-V sur A
        tp = sum(1 for i in gids if "A" in key[i] and "A" in gold[i])
        fp = sum(1 for i in gids if "A" in key[i] and "A" not in gold[i])
        fn = sum(1 for i in gids if "A" not in key[i] and "A" in gold[i])
        p = tp / (tp + fp) if tp + fp else float("nan")
        r = tp / (tp + fn) if tp + fn else float("nan")
        ok = p >= 0.8 and r >= 0.8
        print(f"\nVerdict H-V (précision ET rappel de A >= 0,8) : "
              f"{'POSITIF' if ok else 'NÉGATIF'} (P={p:.2f}, R={r:.2f})")


if __name__ == "__main__":
    main()
