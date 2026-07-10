# F3 campagne 1 — annotation humaine (grammaire I1 v0.2)

**Pré-enregistrement** : `docs/PREREGISTREMENT_F3.md` (gelé avant ouverture
des données, commit `af2ecd6`). **Guide des juges** :
`docs/GUIDE_ANNOTATION_F3.md` (gelé). Issue : X-48.

## Contenu

- `make_sample.py` — tirage déterministe de l'échantillon (seed 20260706,
  300 clauses stratifiées, sur-échantillonnage de la classe A à 30 %).
  Exige les données du pilote (`../pilote_f3/data/` et
  `../pilote_f3/recettes/content/`, cf. README du pilote). Ne pas relancer :
  le tirage est unique, les fichiers tirés sont commités.
- `sample_annotation.csv` — la feuille EN AVEUGLE à remettre aux juges
  (aucune origine de corpus, aucune étiquette machine).
- `sample_key.csv` — ⚠️ la clé (strate + prédictions du classifieur). À ne
  montrer à AUCUN juge avant la fin de l'adjudication.
- `kappa.py` — accord inter-juges (κ de Cohen, IC bootstrap) + validation de
  l'instrument contre l'or adjudiqué (précision/rappel, IC de Wilson).

## Procédure pour les juges (≥ 2)

1. Chaque juge reçoit une copie de `sample_annotation.csv` (par ex.
   `juge1.csv`, `juge2.csv`) et le guide `GUIDE_ANNOTATION_F3.md`. Lire le
   guide EN ENTIER avant de commencer, y compris les cas limites (§4).
2. Annoter seul, sans se concerter, dans l'ordre du fichier. Remplir la
   colonne étiquettes avec une ou plusieurs classes parmi `A,I,C,N,OTHER`
   (multi autorisé, ex. `I,C`). Vide = OTHER. Tout cas douteux : annoter
   quand même + note en colonne commentaire (il nourrira l'adjudication,
   jamais une révision rétroactive du guide).
3. Quand les DEUX feuilles sont remplies :
   `python3 kappa.py juge1.csv juge2.csv` → verdict **H-κ** (κ(A) ≥ 0,7).
4. Adjudication des désaccords à trois (consignée dans `adjudication.md`),
   production de `gold.csv` (même format), puis :
   `python3 kappa.py juge1.csv juge2.csv --gold gold.csv` → verdict **H-V**
   (précision ET rappel de A ≥ 0,8 pour que les chiffres corpus du pilote
   deviennent citables).

## Ce que cette campagne ne mesure PAS

Les taux de classes (P1/P2a/P2b) : l'échantillon sur-représente A par
construction. Les taux restent mesurés corpus entiers par le classifieur
(`../pilote_f3/`), qui n'est citable qu'après un H-V positif.
