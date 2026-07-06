# Pilote F3 — provenance et statut

Étude complémentaire externe reçue le 2026-07-06 (transmise par Reda), intégrée après
vérification d'alignement. **Statut : pilote** — classifieur à règles + audit manuel à
un seul juge, anglais uniquement, non pré-enregistré par le projet. Il ne remplace PAS
le F3 du noyau (juges humains indépendants, pré-enregistrement) ; il montre que la
conjecture SURVIT au premier contact avec des corpus réels.

- Résultats et analyse : `docs/RESULTATS_PILOTE_F3.md`
- Grammaire opérationnalisée : `i1_classifier.py` (les 4 classes de
  `docs/I1_grammaire_fragment_invariant.md`)
- Reproduction : `python3 run_pilote.py` — exige un dossier `data/` NON inclus
  (e-SNLI, CoS-E v1.11, LIAR-PLUS, à télécharger depuis leurs dépôts officiels).
- Vérification faite à l'intégration : cohérence interne `resultats.json` ↔ chiffres du
  rapport (lift 57,6 ; A e-SNLI 0,21 % ; LIAR 22,0 % ; part-calibration 23,8 %) — OK.
  Ré-exécution locale non faite (données absentes) : à refaire avant toute citation
  dans le papier.

## 2e livraison (v2)

- `run_recettes.py` : registre intermédiaire (based.cooking, 350 recettes — données NON
  incluses, dossier `recettes/content/` à télécharger). Prédiction pré-enregistrée au §8
  de la v1, confirmée (§9 du rapport).
- `i1_classifier.py` mis à jour : dates à barres = 3 composantes obligatoires (fix
  fractions), unités de cuisine, températures — diff vérifié à l'intégration, conforme
  au rapport.
- ⚠️ `resultats.json` reste celui du run v1 (avant correctif) : à régénérer lors de la
  ré-exécution locale. Chiffres v2 : dans le rapport (`docs/RESULTATS_PILOTE_F3.md`).
