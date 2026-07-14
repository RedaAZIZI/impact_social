# Taxonomie des échecs EPIC-0 (X-60)

Runs analysés : `brute-v1`, `direct-haiku`, `direct-sonnet` — seuil near_miss < 5% de cellules fausses.

## Masses par catégorie

| catégorie | brute-v1 | direct-haiku | direct-sonnet |
|---|---|---|---|
| parse_error | 0 | 2 | 0 |
| timeout | 0 | 0 | 11 |
| wrong_size | 0 | 8 | 3 |
| near_miss | 0 | 11 | 12 |
| wrong_colors | 0 | 11 | 2 |
| structure_missed | 192 | 75 | 41 |

## Croisement des runs

- Échecs communs aux 3 solveurs : **57**
- Échecs propres à `brute-v1` : 74
- Échecs propres à `direct-haiku` : 1
- Échecs propres à `direct-sonnet` : 0

## Exemples par catégorie (run de référence : `direct-sonnet`)

### parse_error

- `arc1/training/b60334d2` (direct-haiku) — aucune sortie exploitable (statut parse_error)
- `arc1/training/db93a21d` (direct-haiku) — aucune sortie exploitable (statut parse_error)

### timeout

- `arc1/training/0e206a2e` (direct-sonnet) — aucune sortie exploitable (statut timeout)
- `arc1/training/1a07d186` (direct-sonnet) — aucune sortie exploitable (statut timeout)
- `arc1/training/239be575` (direct-sonnet) — aucune sortie exploitable (statut timeout)

### wrong_size

- `arc1/training/1190e5a7` (direct-sonnet) — forme produite (4, 15) ≠ attendue (5, 3) (input (22, 22))
- `arc1/training/234bbc79` (direct-sonnet) — forme produite (3, 9) ≠ attendue (3, 8) (input (3, 11))
- `arc1/training/91413438` (direct-sonnet) — forme produite (18, 18) ≠ attendue (21, 21) (input (3, 3))

### near_miss

- `arc1/training/00d62c1b` (direct-sonnet) — forme correcte, 0.2% de cellules fausses
- `arc1/training/045e512c` (direct-sonnet) — forme correcte, 4.1% de cellules fausses
- `arc1/training/2c608aff` (direct-sonnet) — forme correcte, 0.3% de cellules fausses

### wrong_colors

- `arc1/training/72ca375d` (direct-sonnet) — forme correcte, 100.0% de cellules fausses
- `arc1/training/75b8110e` (direct-sonnet) — forme correcte, 31.2% de cellules fausses

### structure_missed

- `arc1/training/025d127b` (direct-sonnet) — forme correcte, 10.0% de cellules fausses
- `arc1/training/150deff5` (direct-sonnet) — forme correcte, 6.8% de cellules fausses
- `arc1/training/1b60fb0c` (direct-sonnet) — forme correcte, 19.0% de cellules fausses

## Primitives DSL v1 candidates (≤ 10)

Comptées sur les 57 échecs communs aux 3 solveurs — une tâche peut être expliquée par plusieurs primitives.

| primitive candidate | catégorie débloquée | tâches expliquées |
|---|---|---|
| fill_background (remplissage du fond) | structure_missed | 26 |
| symmetrize (complétion de symétrie) | structure_missed | 1 |
| extract_object (segmentation en objets) | wrong_size | 1 |
| select_subgrid (sélection de sous-grille) | wrong_size | 1 |
