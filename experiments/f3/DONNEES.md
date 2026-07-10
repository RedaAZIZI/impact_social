# F3 campagne 1 — fiche descriptive des données (standard « pas de CSV sur GitHub »)

**Standard de données du projet (décision Reda, 2026-07-08).** Le repo GitHub ne porte
plus de fichiers `.csv`. Chaque table de données vit hors repo (Google Drive / Google
Sheets) ; le repo porte à la place une **fiche descriptive** `.md` qui déclare, pour
chaque table : colonnes et types, clés primaire/étrangères, lien vers le fichier,
propriétaire, empreinte SHA-256 quand le contenu est gelé, et procédure de contrôle
d'intégrité au retour. **Exception d'antériorité** : les CSV commités AVANT le standard
(`sample_annotation.csv`, `sample_key.csv`, PR #6) restent en place — leur commit fait
foi d'horodatage du gel pré-enregistré ; migration éventuelle = décision de Reda après
merge de la PR #6.

## Déclaration des tables

### T1 — `sample_annotation` (feuille en aveugle, GELÉE)

- **Emplacement** : repo, `experiments/f3/sample_annotation.csv` (antériorité PR #6).
- **SHA-256** : `545df573a44d0912d2ebe2b64045c65ab953bbca73cea8d141620bfebc456dbf`.
- **Lignes** : 300 (F3-001 → F3-300) + en-tête. Encodage UTF-8, fins de ligne CRLF.
- **Colonnes** :
  | # | nom | type | contrainte |
  |---|---|---|---|
  | 1 | `id` | texte `F3-NNN` | **clé primaire** (c'est la clé de jointure de `kappa.py`) |
  | 2 | `clause` | texte | la clause TELLE QU'AFFICHÉE fait foi (guide §1) |
  | 3 | `etiquettes` | ensemble ⊆ {A,I,C,N,OTHER} | à remplir par le juge ; multi séparées par virgules ; vide = OTHER |
  | 4 | `commentaire` | texte libre | cas douteux → note pour l'adjudication |

### T2 — `sample_key` (la clé — SENSIBLE)

- **Emplacement** : repo, `experiments/f3/sample_key.csv` (antériorité PR #6).
- **SHA-256** : `709c88823dab4b3d595a2438bd42af1775d7c916620d71c738b85e36249ed798`.
- ⚠️ **À ne montrer à AUCUN juge avant la fin de l'adjudication** (aveugle).
- **Colonnes** : `id` (FK → T1.id) ; `strate` (e-snli | liar | recettes-ingredients |
  recettes-etapes) ; `clf_tags` (étiquettes du classifieur, multi) ; `clf_excl`
  (classe exclusive A>I>C>N>OTHER) ; `clf_sub` (sous-marqueurs, ex. `A:measure`).

### T3 — `juge1` (feuille d'annotation du juge 1 = Reda) — **Google Sheet**

- **Lien** : https://docs.google.com/spreadsheets/d/1UzqsPYWF0NJF64Jg-BpBklkljotbOkDpoBhazOMAo0U/edit
- **Propriétaire** : redatln19@gmail.com. **Schéma** : identique à T1 (le juge ne
  remplit que `etiquettes` et `commentaire` ; `id` et `clause` ne se modifient pas).
- **Anomalie connue à la création** (2026-07-08) : une ligne parasite `F` (vide) en
  toute fin de feuille, artefact du transfert — à supprimer à la première ouverture ;
  le contrôle de retour l'élimine de toute façon (voir procédure).
- **Contrôle d'intégrité au retour (OBLIGATOIRE avant `kappa.py`)** : exporter la
  feuille en CSV, puis vérifier (1) l'ensemble des `id` = exactement ceux de T1
  (toute ligne d'id inconnu est rejetée), (2) la colonne `clause` inchangée vis-à-vis
  de T1 à l'octet près (sinon, la divergence est documentée avant tout calcul),
  (3) `etiquettes` ⊆ {A,I,C,N,OTHER}.

### T4 — `juge2` (feuille du juge 2) — **à créer**

- Création par COPIE Drive de la feuille vierge (mêmes règles que T3), au moment où
  le juge 2 est recruté. Le juge 2 ne voit ni T2, ni T3 (annotation indépendante).

### T5 — `gold` (or adjudiqué) — **à créer après adjudication**

- Schéma de T1, produit par l'adjudication à trois (consignée dans
  `adjudication.md`). Sert au verdict H-V via `kappa.py --gold`.

### Hors périmètre du standard

`resultats.json`, `samples_audit.txt` (artefacts de code, non tabulaires) restent
dans le repo. Les données corpus brutes (e-SNLI, LIAR…) ne sont jamais commitées
(`.gitignore` du pilote) — dépôts officiels référencés dans le README du pilote.
