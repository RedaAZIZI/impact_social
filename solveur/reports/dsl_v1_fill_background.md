# DSL v1 — mesure fill_background sur la liste gelée (X-62)

Hypothèse et seuil de falsification fixés dans le ticket X-62 **avant** le code :
étendre la DSL avec `fill_enclosed(c)` (a) et `fill_holes_per_object(c)` (b),
les deux stratégies dans l'espace de recherche ; hypothèse falsifiée si le
brute-force étendu résout **moins de N = 5 des 26 tâches** `fill_background`
gelées (échecs communs aux 3 runs EPIC-0, extraites de
`data_gel/runs_epic0.db.gz` après vérification SHA-256 conforme à `DONNEES.md`).

Run de mesure : `brute-v2` (split dev, 200 tâches, coût 0 $, git_sha `264cbcd`).

## Verdict : hypothèse FALSIFIÉE (1/26 < N = 5)

| mesure | valeur |
|---|---|
| tâches gelées résolues | **1/26** (`00d62c1b` → `fill_enclosed(4)`) |
| gain hors liste gelée | 1 (`d5d6de2d` → `fill_enclosed(3) ∘ recolor(2→0)`) |
| score global | 5,0 % (10/200) vs 4,0 % brute-v1 |
| non-régression brute-v1 | **8/8 conservées**, programmes identiques |
| timeouts (120 s) | 7, aucun sur la liste gelée ni sur les 8 brute-v1 |
| durée | 3 668 s (18,3 s/tâche) vs 581 s brute-v1 |

## Lecture

1. **Une catégorie de taxonomie n'est pas une primitive.** Le détecteur
   `_detect_fill_background` (« seules des cellules de fond changent ») est une
   borne optimiste : sur les 26 tâches compatibles, une seule est un remplissage
   *à couleur constante* de régions encloses. Les autres exigent des paramètres
   calculés depuis la grille : couleur fonction de la taille ou de la forme du
   trou, motifs à propager, tracés dépendants du contexte.
2. **La composition travaille.** `d5d6de2d` (hors liste) tombe par
   `fill_enclosed(3) ∘ recolor(2→0)` — gain non ciblé, produit par la
   combinatoire, exactement le mécanisme espéré.
3. **Le coût combinatoire condamne l'extension aveugle du brute-force.**
   Deux familles de primitives en plus : ×6,3 sur la durée du run (après
   vectorisation du flood-fill). Chaque famille paramétrée multiplie l'espace ;
   c'est l'argument empirique pour T-1.3 (le LLM propose, le vérifieur dispose)
   plutôt que pour empiler des variantes dans l'énumération.

## Conséquence pour la suite (EPIC-1)

Le palier suivant n'est pas « plus de variantes de fill » mais des primitives
objectales dont les paramètres sont *calculés* depuis la grille — à faire
proposer par le LLM (T-1.3) et vérifier par l'interpréteur, pas énumérer.
