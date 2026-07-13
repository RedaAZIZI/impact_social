# Gel des données EPIC-0 — runs.db

**Exception temporaire et documentée au standard de données (décision Reda, 2026-07-08).**
Le conteneur d'exécution agent est éphémère : sans ce gel, la base `runs.db` des runs
officiels EPIC-0 (dont les prédictions LLM, non regénérables sans repayer ~11 $)
serait perdue à la fin de la session. À déplacer vers Google Drive puis supprimer
du repo, conformément au standard.

## Fichier

- `runs_epic0.db.gz` — gzip de `solveur/runs.db` au gel du 2026-07-13 (fin EPIC-0).
- SHA-256 du `.gz` : `c243bf0522a02fddff7ed64512b4e8bd498f5fe31f573d9749d65594528ab76d`
- SHA-256 du `runs.db` décompressé : `b0b6d13c74d103f009105b98b7374913a04e316b33ff4e9098a9576fda384cbb`
- Contrôle d'intégrité au retour : `gunzip -k runs_epic0.db.gz && sha256sum runs_epic0.db`
- Propriétaire : Reda Azizi (redatln19@gmail.com)

## Schéma

### `runs` (4 lignes)
| colonne | type | description |
|---|---|---|
| run_id | TEXT PK | `brute-v1`, `direct-haiku`, `direct-sonnet`, `direct-haiku-1783910419` (test de plomberie, 3 tâches) |
| solver_name | TEXT | brute / direct-haiku / direct-sonnet |
| git_sha | TEXT | commit du code au moment du run |
| split | TEXT | `dev` (200 tâches) |
| started_at, score, n_tasks, n_solved, cost_usd, duration_s | | métriques agrégées |

### `task_results` (~603 lignes)
| colonne | type | description |
|---|---|---|
| run_id, task_id | TEXT PK | ex. `arc1/training/00d62c1b` |
| status | TEXT | solved / failed / timeout / parse_error |
| duration_s, cost_usd, n_attempts | | par tâche |
| meta_json | TEXT | **grilles prédites** (`attempts`), hash et réf du prompt, parse_errors — intrant de T-1.0 (taxonomie des échecs) |

## Contenu (résumé)

| run | score | coût |
|---|---|---|
| brute-v1 | 4,0 % (8/200) | 0 $ |
| direct-haiku | 46,5 % (93/200) | 2,67 $ |
| direct-sonnet | 65,5 % (131/200) | 8,60 $ |
