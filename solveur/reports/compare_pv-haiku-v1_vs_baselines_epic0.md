# pv-haiku-v1 vs les 3 baselines EPIC-0 — verdict X-64

Hypothèse et critère de falsification gelés dans le ticket X-64 (validés par Reda
le 2026-07-13, **avant** le code du solveur) : falsifié si le score dev complet
est < 15 % avec Haiku et k ≤ 8 propositions/tâche.

Run officiel : `pv-haiku-v1` (split dev, 200 tâches, k=8, prompt gelé
`propose_v1`, git_sha `c5200e0`). Palier 1 (`pv-haiku-p1`, 20 tâches, k=4) :
0/20, voir `run_pv-haiku-p1.md`. SHA-256 de `data_gel/runs_epic0.db.gz` et du
`runs.db` décompressé vérifiés conformes à `DONNEES.md` avant les runs.

## Verdict : hypothèse FALSIFIÉE (4,5 % < 15 %)

| run | score | coût | s/tâche |
|---|---|---|---|
| **pv-haiku-v1** | **4,5 % (9/200)** | 2,36 $ | 15,1 |
| brute-v1 | 4,0 % (8/200) | 0 $ | 2,9 |
| brute-v2 (X-62) | 5,0 % (10/200) | 0 $ | 18,3 |
| direct-haiku | 46,5 % (93/200) | 2,67 $ | — |
| direct-sonnet | 65,5 % (131/200) | 8,60 $ | — |

À coût comparable (≈ 2,4 $ vs 2,7 $), proposer-vérifier fait ×10 moins bien que
la prédiction directe de grilles par le même modèle — mais chacune de ses
9 réponses est accompagnée d'un programme lisible vérifié sur tout le train
(100 % des soumissions, conformément à l'hypothèse), quand les 93 réponses de
direct-haiku sont des grilles opaques.

## Chiffres du run

| mesure | valeur |
|---|---|
| programmes proposés (uniques, parsés) | 1 009 (5,0/tâche) |
| vérifiés (reproduisent tout le train) | 10 |
| rejets « ne reproduit pas le train » | 999 (99,0 % des parsés) |
| rejets de parse (vide / syntaxe) | 469 |
| plafonds | 2,36 $ < 3 $ ; aucun dépassement par tâche |

## Recouvrement avec les baselines

- **7 des 8 tâches brute-v1** retrouvées (programmes identiques ou équivalents).
- **2 gains hors brute-v1** : `d511f180` (`recolor(5→0) | recolor(8→5) | recolor(0→8)`,
  une permutation de couleurs en 3 pas — hors de portée de l'énumération à cette
  profondeur) et `d5d6de2d` (`fill_holes_per_object(3) | recolor(2→0)`,
  équivalent au programme brute-v2).
- **1 manque** : `f25fbde4` (brute : `crop_to_content | scale(2)`). Near-miss
  révélateur : 11 propositions contiennent toutes le bon préfixe
  `crop_to_content | scale(2)` mais y greffent systématiquement un `tile(2,2)`
  superflu — le LLM voit la bonne transformation et la sur-complique.
- Aucune tâche résolue par pv-haiku seul contre les 3 baselines réunies.
- 8/9 solutions sont aussi dans direct-haiku et direct-sonnet.

## Lecture

1. **La falsification est nette et propre.** 4,5 % ≪ 15 % : « proposer-vérifier
   > énumération à coût comparable » est faux **pour la DSL v1**. Le gain réel
   sur l'énumération est marginal (+1 vs brute-v1, −1 vs brute-v2) pour 2,36 $.
2. **Le goulot est l'expressivité, pas le mécanisme.** 99 % des programmes
   parsés échouent au train : Haiku propose des programmes plausibles dans une
   DSL qui ne peut pas exprimer les solutions (verdict X-62 confirmé à
   l'échelle). Quand la DSL suffit, le pipeline trouve — y compris une
   composition de profondeur 3 inaccessible au brute-force.
3. **La promesse d'explicabilité tient.** 100 % des réponses soumises sont
   accompagnées d'un programme vérifié sur tout le train — c'est la moitié de
   l'hypothèse qui survit, et l'argument produit du PoC.
4. **Taux de parse à surveiller** : 469 rejets de parse (≈ 32 % des extractions)
   — matière pour durcir le prompt en v2, sans enjeu sur le verdict.

## Conséquence (prévue par le ticket)

La matière passe à **l'extension objectale de la DSL** avant tout nouveau run :
primitives sur objets segmentés dont les paramètres sont *calculés* depuis la
grille (couleur fonction de la taille du trou, déplacements relatifs entre
objets, propagation de motifs) — ce que ni l'énumération ni la DSL v1 ne
peuvent exprimer, et que le near-miss `f25fbde4` comme les 999 rejets train
désignent comme le vrai verrou.
