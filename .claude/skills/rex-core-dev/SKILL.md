---
name: rex-core-dev
description: Développer, refactorer ou étendre le moteur /core (librairie rex) du projet REX. Utiliser quand l'utilisateur demande de développer le moteur, ajouter à /core, ou modifier RuleListModel / les opérateurs W et W⁻¹.
---

# Développement de la librairie `rex` (/core)

`core/rex` est le futur moteur produit : chaque avancée de recherche doit y atterrir sous forme d'API propre et testée.

## API actuelle

- `rex.models` : `RuleListModel` (liste ordonnée de règles, sémantique premier-match, `firing_rule` = carte de localité), `rule_membership`.
- `rex.why` : opérateur W — `extract_rule(tree, x)` (règle minimale décidant x), `extract_rules(tree)`.
- `rex.edit` : opérateur W⁻¹ — `edit_rule`, `edit_where` (une phrase sémantique → toutes les règles d'un concept).
- `rex.metrics` : `fidelity`, `fidelity_curve` (courbe d'explicabilité dans une base récepteur), `explainability_auc`, `random_rotation`.

## Invariants à préserver (non négociables)

1. **L'édition est locale par construction** : éditer la règle i ne peut changer les prédictions que là où `firing_rule(X) == i`. Le test `tests/test_edit.py::test_edit_is_local_by_construction` le vérifie — il doit rester vert après toute modification. C'est l'argument « zéro oubli catastrophique » du papier : ne jamais introduire un mécanisme d'édition qui casse cette garantie.
2. `RuleListModel.from_tree` reproduit l'arbre **exactement** (les règles partitionnent l'espace).
3. La règle rendue par W est **minimale** (chemin de décision, aucun prédicat superflu) et exprimée dans le vocabulaire du récepteur (prédicats à seuil).

## Politique de dépendances et style

- Phases 1-2 : **numpy, scikit-learn, scipy uniquement**. Refuser toute nouvelle dépendance sans arbitrage (voir `docs/STRATEGIE.md`).
- Python ≥ 3.10. Chaque fonction publique a une docstring ; chaque ajout d'API vient avec ses tests dans `/tests`.
- Les scripts de `/experiments` consomment la librairie, jamais l'inverse.
- Lancer `python -m pytest tests/` avant tout commit.
