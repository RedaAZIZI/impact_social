# Expériences

Chaque script est autonome, reproduit ses résultats de zéro (seeds fixées) et sauvegarde ses sorties numériques dans `experiments/results/` (ignoré par git). Dépendances : numpy, scikit-learn, scipy.

Protocole standard du projet : hypothèse écrite AVANT l'expérience, critère de falsification a priori, multi-seeds (≥5), moyenne ± écart-type.

| Script | Expérience | Hypothèse testée | Résultat |
|---|---|---|---|
| `exp1_solid.py` | Exp 1 (10 seeds) | Le coût d'explicabilité croît avec le désalignement des bases (rotations expm(θA), θ ∈ {0, 0.2, 0.4, 0.8, 1.5}) | AUC 0.918 → 0.745, monotonie stricte ; critère de falsification (courbes superposées) passé |
| `exp2.py` | Exp 2 (5 seeds) | La reconstruction de M par questions W converge en base alignée, pas en base désalignée | 6 questions → 92 % aligné ; plafond ~71 % à θ=1.5 |
| `exp3.py` | Exp 3 (5 seeds) | Une phrase d'édition (W⁻¹) vaut plus que le fine-tuning après concept drift | Édition : 0.990 ; fine-tuning 3000 exemples : 0.968 |
| `exp1b_exp4.py` | Exp 1b + Exp 4 (5 seeds) | 1b : le coût vient du mélange des dimensions, pas de leur reparamétrisation monotone ; 4 : l'explicabilité dépend de la question Q | 1b : AUC identique linéaire vs tanh (0.743) ; 4 : taille de réponse 2.95 → 6.39 selon Q, asymétrique |

Le monde synthétique de référence : 6000 objets, 5 attributs ~ U[0,1] (taille, teinte, forme, pos_x, pos_y), graphe vrai G\* écrit à la main (~7 branches), modèle opaque M = MLP 2×50 (accuracy 0.976 ± 0.006).

Résultats détaillés, tableaux complets et interprétations : `docs/article_source_explicabilite.md` (sections 5 à 9).
