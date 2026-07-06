# -*- coding: utf-8 -*-
"""Test du registre intermédiaire : recettes (based.cooking, 350 fichiers).
Prédiction pré-enregistrée (RESULTATS_PILOTE_F3.md §8) :
  - A concentré dans les lignes d'INGRÉDIENTS (quantité+unité = calibration) ;
  - dans les ÉTAPES, l'ossature est I (ordre : until/then/before/after),
    les A restants étant temps/températures (calibrations locales)."""
import glob, math, re
from collections import Counter
from i1_classifier import classify

def wilson(k, n, z=1.96):
    if n == 0: return (0, 0, 0)
    p = k/n; d = 1+z*z/n
    c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return (p, max(0, c-h), min(1, c+h))

SPLIT = re.compile(r"(?<=[.!?])\s+")
ing_lines, step_sents = [], []
for fn in glob.glob("recettes/content/*.md"):
    if fn.endswith("_index.md"): continue
    txt = open(fn, encoding="utf-8").read()
    sec = None
    for line in txt.splitlines():
        l = line.strip()
        if l.lower().startswith("## ingredient"): sec = "ing"; continue
        if l.lower().startswith("## direction"): sec = "dir"; continue
        if l.startswith("##"): sec = None; continue
        if not l or sec is None: continue
        l = re.sub(r"^[-*]\s+|^\d+[.)]\s+", "", l)
        if len(l.split()) < 2: continue
        if sec == "ing": ing_lines.append(l)
        else: step_sents.extend(s for s in SPLIT.split(l) if len(s.split()) >= 3)

def report(items, name):
    n = len(items); cnt = Counter(); subs = Counter()
    for s in items:
        r = classify(s)
        for k, v in r["tags"].items():
            if v: cnt[k] += 1
        for sb in r["sub"]: subs[sb] += 1
    print(f"\n### {name} — n = {n}")
    for k in ["A", "I", "C", "N"]:
        p, lo, hi = wilson(cnt.get(k, 0), n)
        print(f"  contient {k}: {100*p:5.1f}% [IC95 {100*lo:.1f}-{100*hi:.1f}] ({cnt.get(k,0)})")
    print("  sous-marqueurs:", subs.most_common(8))
    return cnt, n

ci, ni = report(ing_lines, "Lignes d'ingrédients")
cs, ns = report(step_sents, "Phrases d'étapes (directions)")
print(f"\nRatio A ingrédients/étapes : {(ci['A']/ni)/(cs['A']/ns):.1f}x")
print(f"Part de I:ordre dans les étapes : "
      f"{100*Counter(sb for s in step_sents for sb in classify(s)['sub'])['I:ordre']/ns:.1f}%")
