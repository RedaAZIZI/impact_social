# Reproductibilité — inventaire de la fondation (état au 2026-07-06, session du pivot)

**Rôle du document** : recenser ce qui se reproduit, avec quelles commandes, et ce que
chaque élément apporte à la nouvelle direction (axe REX-Géo). C'est l'inventaire demandé
par la décision de pivot (« l'existant = source d'évolution »).

## Vérifications de cette session

| Élément | Commande | Résultat (2026-07-06) |
|---|---|---|
| Suite de tests /core (10 tests, dont l'invariant de localité de l'édition) | `python -m pytest tests/ -q` | **10/10 verts** (1.5 s) |
| Exp 1b/4 relancée de zéro (agent de reproductibilité, workflow) | `python experiments/exp1b_exp4.py` | voir tableau ci-dessous |

## Inventaire des éléments reproductibles et leur rôle dans REX-Géo

| Élément | Script (seeds fixées) | Résultat de référence | Rôle pour la nouvelle direction |
|---|---|---|---|
| Exp 1 — coût vs désalignement | `experiments/exp1_solid.py` | AUC 0.918 (θ=0) → 0.745 (θ=1.5), 10 seeds | Mesure du coût HORS-G (le mélange) — donnée pour [C 1.5] (loi des angles principaux) |
| Exp 1b — invariance monotone | `experiments/exp1b_exp4.py` | AUC 0.7432/0.7433/0.7433 (linéaire/tanh) | **Instance empirique de T1** — le groupe d'invariance mesuré ; 11/11 runs confirmés (BILAN) |
| Exp 2 — protocole W | `experiments/exp2.py` | 6 questions → 92 % aligné ; plafond ~71 % désaligné | Décodage interactif du canal ([P 3.3]) |
| Exp 3 — W⁻¹ vs fine-tuning | `experiments/exp3.py` | 0.990 vs 0.968 (3000 exemples) | Le canal invariant bat le gradient — argument de maintenabilité de la KB |
| Exp 4 — dépendance à Q | `experiments/exp1b_exp4.py` | taille contrastive 2.95 → 6.39 | Donnée pour F4 (le contexte comme distribution de questions) |
| Exp 5 — German Credit | `experiments/exp5_german_credit.py` | écart −0.003 ± 0.019 (infirmation propre) | Preuve de discipline (les infirmations se publient) ; borne du désalignement naturel |
| Exp 6 — AI4I 2020 | `experiments/exp6_predictive_maintenance.py` | +0.045 ± 0.010 (MLP), nul (GBT) | Désalignement naturel réel ; l'écart dépend de la base interne de M |
| Exp 7 — le graphe qui vit | `experiments/exp7_living_graph.py` | 15 phrases > 75 000 étiquettes ; 0.990 ± 0.003 | Localité de l'édition à l'échelle du régime interactif — préfigure la KB |
| Librairie `/core` (rex) | `pip install -e core` ; voir skill rex-core-dev | API : RuleListModel, W, W⁻¹, métriques | Le substrat qui deviendra le noyau ℛ + KB (quand I1/F7 le forceront) |
| Données réelles | `data/` (scripts UCI, rien de commité) | German Credit, AI4I 2020 | Bancs d'essai de validation |

## Règles

1. Chaque script régénère ses résultats de zéro (seeds fixées) ; toute divergence par
   rapport aux chiffres de référence est un incident à documenter, pas à ignorer.
2. La grille de seuils discrétisée V_δ explique les résidus ~10⁻⁴ de l'Exp 1b
   (remarque (b) de T1, `docs/preuves_invariance.md`).
3. Le tableau « rôle pour la nouvelle direction » applique la règle de recyclage
   anti-patchwork : chaque réutilisation passe par cette relecture géométrique — pas de
   transplantation par défaut.
