# -*- coding: utf-8 -*-
"""Pilote F3 — analyse des trois corpus réels."""
import csv, json, math, random, re, sys
from collections import Counter
from i1_classifier import classify, tokenize, RE_NUM, NUMWORDS

random.seed(42)
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0, c - h), min(1, c + h))


def has_numeral(text):
    return any(RE_NUM.fullmatch(t) or t in NUMWORDS for t in tokenize(text))


# ------------------------------------------------------------------ e-SNLI --
esnli = []   # (explication, input_has_num)
for fn in ["data/esnli_dev.csv", "data/esnli_test.csv"]:
    with open(fn, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            e = (row.get("Explanation_1") or "").strip()
            if len(e.split()) < 3:
                continue
            inp = (row.get("Sentence1", "") + " " + row.get("Sentence2", ""))
            esnli.append((e, has_numeral(inp)))

# ------------------------------------------------------------------- CoS-E --
cose = []
with open("data/cose_dev.jsonl", encoding="utf-8") as f:
    for line in f:
        try:
            d = json.loads(line)
            e = (d.get("explanation", {}).get("open-ended") or "").strip()
            if len(e.split()) >= 3:
                cose.append(e)
        except json.JSONDecodeError:
            pass

# --------------------------------------------------------------- LIAR-PLUS --
liar_sents = []
for fn in ["data/liar_val2.tsv", "data/liar_test2.tsv"]:
    with open(fn, encoding="utf-8") as f:
        for line in f:
            cols = line.rstrip("\n").split("\t")
            if len(cols) < 16:
                continue
            just = cols[15].strip()
            if not just or just.lower() == "nan":
                continue
            for s in SENT_SPLIT.split(just):
                if len(s.split()) >= 4:
                    liar_sents.append(s.strip())


def run(sents, name):
    n = len(sents)
    counts = Counter()
    excl = Counter()
    subs = Counter()
    samples = {k: [] for k in ["A", "I", "C", "N", "OTHER"]}
    calib_and_A = 0
    idx = list(range(n))
    random.shuffle(idx)
    results = []
    for s in sents:
        r = classify(s)
        results.append(r)
        for k, v in r["tags"].items():
            if v:
                counts[k] += 1
        excl[r["excl"]] += 1
        for sb in r["sub"]:
            subs[sb] += 1
        if r["tags"]["A"] and r["calib_shaped"]:
            calib_and_A += 1
    for i in idx:
        e = results[i]["excl"]
        if len(samples[e]) < 20:
            samples[e].append((sents[i], results[i]["sub"]))
    return {"name": name, "n": n, "counts": dict(counts), "excl": dict(excl),
            "subs": subs.most_common(25), "samples": samples,
            "calib_and_A": calib_and_A, "results": results}


r_esnli = run([e for e, _ in esnli], "e-SNLI (explications)")
r_cose = run(cose, "CoS-E (explications)")
r_liar = run(liar_sents, "LIAR-PLUS (justifications fact-check)")

print("=" * 78)
for r in (r_esnli, r_cose, r_liar):
    n = r["n"]
    print(f"\n### {r['name']}  —  n = {n} phrases")
    for k in ["A", "I", "C", "N"]:
        p, lo, hi = wilson(r["counts"].get(k, 0), n)
        print(f"  contient {k}: {100*p:5.1f}%  [IC95 {100*lo:.1f}–{100*hi:.1f}]"
              f"  ({r['counts'].get(k, 0)})")
    print(f"  composition exclusive (A>I>C>N>OTHER): "
          + "  ".join(f"{k}={100*r['excl'].get(k,0)/n:.1f}%"
                      for k in ["A", "I", "C", "N", "OTHER"]))
    a = r["counts"].get("A", 0)
    if a:
        print(f"  parmi les phrases A : forme-calibration = "
              f"{100*r['calib_and_A']/a:.1f}% ({r['calib_and_A']}/{a})")
    print("  sous-marqueurs dominants:", r["subs"][:10])

# ---------------- test de concentration (P2, intra e-SNLI) ----------------
print("\n" + "=" * 78)
print("### Test P2 intra-corpus (e-SNLI) : A dans l'explication conditionné")
print("### à la présence d'un numéral dans (prémisse+hypothèse)")
grp = {True: [0, 0], False: [0, 0]}
for (e, inum), res in zip(esnli, r_esnli["results"]):
    grp[inum][1] += 1
    if res["tags"]["A"]:
        grp[inum][0] += 1
for cond in (True, False):
    k, n = grp[cond]
    p, lo, hi = wilson(k, n)
    print(f"  numéral dans l'input={cond!s:5s}: P(A|·) = {100*p:.2f}% "
          f"[{100*lo:.2f}–{100*hi:.2f}]  ({k}/{n})")
pt, pf = grp[True][0] / grp[True][1], grp[False][0] / max(1, grp[False][1])
print(f"  lift = {pt/max(pf,1e-9):.1f}x")

# même chose pour N (comptes)
grpN = {True: [0, 0], False: [0, 0]}
for (e, inum), res in zip(esnli, r_esnli["results"]):
    grpN[inum][1] += 1
    if res["tags"]["N"]:
        grpN[inum][0] += 1
ptN = grpN[True][0] / grpN[True][1]
pfN = grpN[False][0] / grpN[False][1]
print(f"  (contrôle N: P(N|num)={100*ptN:.1f}%  P(N|¬num)={100*pfN:.1f}%  "
      f"lift={ptN/pfN:.1f}x)")

# ---------------- échantillons pour audit manuel ----------------
with open("samples_audit.txt", "w", encoding="utf-8") as f:
    for r in (r_esnli, r_cose, r_liar):
        f.write(f"\n{'='*70}\n{r['name']}\n{'='*70}\n")
        for k in ["A", "I", "C", "N", "OTHER"]:
            f.write(f"\n--- classe {k} ---\n")
            for s, sb in r["samples"][k][:15]:
                f.write(f"  [{','.join(sb)}] {s}\n")
print("\nÉchantillons écrits dans samples_audit.txt")

# résumé JSON pour le rapport
out = {}
for r in (r_esnli, r_cose, r_liar):
    n = r["n"]
    out[r["name"]] = {
        "n": n,
        "rates": {k: wilson(r["counts"].get(k, 0), n)
                  for k in ["A", "I", "C", "N"]},
        "excl": {k: r["excl"].get(k, 0) / n
                 for k in ["A", "I", "C", "N", "OTHER"]},
        "calib_share_of_A": (r["calib_and_A"] / r["counts"]["A"]
                             if r["counts"].get("A") else None),
    }
out["P2_esnli_conditionnel"] = {
    "P(A|num_input)": wilson(*grp[True]),
    "P(A|no_num_input)": wilson(*grp[False]),
    "lift": pt / max(pf, 1e-9),
    "ns": {"num": grp[True][1], "no_num": grp[False][1]},
}
with open("resultats.json", "w") as f:
    json.dump(out, f, indent=2)
