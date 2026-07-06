---
name: rex-experiment
description: Concevoir et lancer une expérience REX (explicabilité relationnelle). Utiliser quand l'utilisateur demande de lancer/designer une expérience REX, de tester une hypothèse du cadre, ou d'étendre les expériences existantes.
---

# Protocole standard d'une expérience REX

Toute expérience suit ce protocole, sans exception :

1. **Hypothèse écrite AVANT l'expérience**, avec un **critère de falsification a priori** (exemple, Exp 1 : « si les courbes de fidélité sont superposées quel que soit θ, le concept d'explicabilité relationnelle est vide »).
2. **Multi-seeds ≥ 5** (10 pour les résultats principaux), rapporter **moyenne ± écart-type**.
3. Script autonome dans `/experiments`, seeds fixées partout, résultats numériques sauvegardés dans `experiments/results/`, figure matplotlib dans `/figures`.
4. Mettre à jour `docs/article_source_explicabilite.md` (tableau de résultats + interprétation) et le README si le résultat est clé.
5. Créer/lier l'issue Linear correspondante (projet REX-P1/P2) avec : hypothèse, critère de falsification, seeds, lien vers le commit.

## Le monde synthétique de référence

- 6000 objets, 5 attributs interprétables ~ U[0,1] : `taille, teinte, forme, pos_x, pos_y`.
- Graphe vrai G\* (vérité terrain explicative, ~7 branches) :
  - SI taille > 0.6 ET teinte > 0.5 → A (0)
  - SINON SI forme > 0.7 → B (1)
  - SINON SI pos_x < 0.3 ET pos_y < 0.3 → A (0)
  - SINON SI teinte < 0.2 ET taille < 0.4 → B (1)
  - SINON → C (2)
- Modèle opaque M : MLP 2×50 (`sklearn`), accuracy ~0.976.
- Récepteur désaligné : base tournée `R = expm(θ·A)` avec A antisymétrique aléatoire normalisée (`rex.metrics.random_rotation`).

## Définitions à respecter

- **Expl(M, R, ε)** = taille minimale d'un graphe de décision exprimé dans le vocabulaire V_R qui simule M à fidélité ≥ 1−ε.
- **Courbe d'explicabilité** : fidélité maximale vs budget (feuilles) ; métrique scalaire = **AUC** (moyenne des fidélités sur les budgets) — `rex.metrics.fidelity_curve` / `explainability_auc`.
- **Opérateur W** : W(x) = règle minimale décidant x (chemin de décision) — `rex.why.extract_rule`. Mesure protocole : nombre de questions W pour reconstruire M à fidélité ε.
- **Opérateur W⁻¹** : édition de règle, locale par construction — `rex.edit`.

## Outils

Réutiliser `core/rex` plutôt que de dupliquer du code dans les scripts. Dépendances autorisées (phases 1-2) : numpy, scikit-learn, scipy, matplotlib. Budgets standard : {2, 4, 8, 16, 32, 64, 128, 256} feuilles.

## Arbitrages

La section « Ce qu'on ne fait PAS maintenant » de `docs/STRATEGIE.md` fait foi : pas de vision/CUB-200 avant conclusion du tabulaire, pas de produit avant le go de phase 2.
