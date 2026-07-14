# DSL v2 objectale — spécification (X-65, palier 0)

Statut : **proposition, en attente de revue par Reda** (palier 0 du ticket X-65).
Rien de ce document n'est codé : l'interpréteur (palier 1) n'existe pas encore et
ne sera écrit qu'après validation explicite de l'hypothèse, du critère de
falsification et de cette spécification.

## 1. Contexte et diagnostic

Verdict X-64 : « proposer-vérifier > énumération à coût comparable » est
**falsifié pour la DSL v1** (4,5 % < 15 % sur le dev complet). Le diagnostic
convergent X-62 + X-64 situe le goulot dans l'**expressivité** du langage, pas
dans le mécanisme :

- 999 des 1 009 programmes proposés par Haiku (99 %) échouent au train — le
  modèle propose des programmes plausibles dans une DSL qui ne peut pas exprimer
  les solutions. (Le `runs.db` de pv-haiku-v1 n'a pas été gelé — conteneur
  éphémère ; la trace exploitable est `reports/run_pv-haiku-v1.md` et le rapport
  comparatif X-64.)
- direct-haiku atteint 46,5 % avec le même modèle : Haiku *voit* les
  transformations ; l'écart de ~40 points est l'espace que la DSL doit combler.
- Sur la liste gelée des 26 tâches `fill_background` (échecs communs aux 3 runs
  EPIC-0, recomputée depuis `data_gel/runs_epic0.db.gz` — SHA-256 vérifiés
  conformes à `DONNEES.md` le 2026-07-14), l'extension aveugle du brute-force
  (X-62) n'en résout qu'une : les 25 autres exigent des **paramètres calculés
  depuis la grille** (couleur fonction d'une propriété de l'objet, motifs à
  propager, tracés dépendant du contexte).

La v1 manipule la grille entière avec des constantes énumérées. La v2 change
l'unité de base : **l'objet** (composante connexe segmentée), avec des
**sélecteurs** et des **paramètres calculés**.

### Liste gelée des 26 `fill_background` (référence de conception)

`00d62c1b, 045e512c, 1b60fb0c, 28e73c20, 2bee17df, 3e980e27, 44d8ac46,
4c5c2cf0, 57aa92db, 5c2c9af4, 6455b5f5, 6cf79266, 6d58a25d, 6e19193c,
7447852a, 83302e8f, aba27056, b27ca6d3, b527c5c6, c1d99e64, d9f24cd1,
db93a21d, ec883f72, f15e1fac, f35d900a, fcc82909` (préfixe `arc1/training/`).

## 2. Principes de conception

1. **v1 ⊂ v2.** Les 12 primitives v1 restent valides telles quelles ; la syntaxe
   pipeline `p1 | p2 | ...` (gauche → droite) est conservée. Tout programme v1
   est un programme v2. Le near-miss `f25fbde4` (`crop_to_content | scale(2)`)
   reste exprimable à l'identique.
2. **Paramètres calculés, pas énumérés.** Les actions acceptent des
   *expressions de propriétés* (`size`, `n_colors`, `minor_color`…) évaluées
   par objet au moment de l'exécution. C'est la réponse directe à la lecture
   X-62 (« une catégorie de taxonomie n'est pas une primitive ») : une
   primitive paramétrée par la grille couvre une famille de tâches, pas une.
3. **Budget : ≤ 15 primitives nouvelles.** La combinatoire de la v2 n'est pas
   destinée à l'énumération (leçon X-62 : ×6,3 de durée pour 2 familles) mais au
   proposeur LLM + vérifieur. Le budget contraint la surface du prompt et le MDL.
4. **Déterminisme total.** Chaque construction a une sémantique unique (ordres,
   égalités, chevauchements, bords : tout est tranché ci-dessous). Même
   programme + même grille = même sortie, toujours.
5. **Explicabilité conservée.** Un programme v2 reste une ligne lisible,
   vérifiable sur tout le train — l'acquis de X-64 (100 % des soumissions
   accompagnées d'un programme vérifié) est non négociable.

## 3. Modèle sémantique

### 3.1 Types

- **Grid** : matrice d'entiers 0-9 (inchangé, `np.int8`, bornes 30×30).
- **Objects** : liste ordonnée d'objets portant chacun ses cellules, sa couleur
  (ou ses couleurs en mode `multi`), sa bbox et ses propriétés dérivées, plus
  une référence à la grille d'origine.

Un programme est un pipeline typé : les primitives v1 sont `Grid → Grid` ; une
primitive de segmentation ouvre un **bloc objet** (`Grid → Objects`) ; `keep`
filtre (`Objects → Objects`) ; une **action** clôt le bloc et rend la grille
(`Objects → Grid`). Le parseur rejette tout pipeline mal typé (action sans
segmentation, segmentation jamais suivie d'action, etc.).

### 3.2 Fond (background)

Couleur la plus fréquente de la grille d'entrée du bloc ; en cas d'égalité,
`0` si présent dans les ex-æquo, sinon le plus petit indice. Le fond est
recalculé à chaque segmentation (la grille peut avoir changé en amont).

### 3.3 Segmentation

Composantes connexes des cellules non-fond. Deux paramètres :

- connexité `4` ou `8` ;
- mode `mono` (défaut : une composante = cellules adjacentes **de même
  couleur**) ou `multi` (une composante = cellules non-fond adjacentes, toutes
  couleurs confondues — pour les objets multicolores type `fcc82909`).

`regions()` segmente au contraire les cellules **de fond** (4-connexité) — les
« pièces » découpées par les murs (`6455b5f5`, `7447852a`).

### 3.4 Ordre et départage (normatif)

- Ordre canonique des objets : coin haut-gauche de bbox (ligne, puis colonne),
  puis taille décroissante. Les actions s'appliquent dans cet ordre ; en cas de
  chevauchement à l'écriture, le dernier écrit gagne.
- `largest`/`smallest` : **tous** les objets atteignant l'extremum (les
  ex-æquo sont tous sélectionnés — requis par `6455b5f5`).
- `rank_size(i)` : rang 1 = plus grand ; ex-æquo départagés par ordre canonique.
- Tout tracé sortant de la grille est **rogné** (jamais d'erreur de bord).
- Un déplacement se fait cellule par cellule ; l'objet est retiré de la grille
  (fond à sa place) avant d'être redessiné à l'arrivée.

## 4. Grammaire

```
programme   ::= etape ("|" etape)*
etape       ::= prim_v1 | segmentation | filtre | action | globale
prim_v1     ::= rotate90 | rotate180 | flip_h | flip_v | transpose
              | crop_to_content | identity | recolor(a->b) | tile(nx,ny)
              | scale(k) | fill_enclosed(c) | fill_holes_per_object(c)

segmentation::= "objects(" conn ("," "multi")? ")" | "regions()"
conn        ::= "4" | "8"
filtre      ::= "keep(" pred ")"
pred        ::= "largest" | "smallest" | "unique_shape" | "unique_color"
              | "touches_edge" | "not_touches_edge" | "has_hole"
              | prop cmp valeur | "rank_size" "==" entier
cmp         ::= "==" | "!=" | ">=" | "<=" | ">" | "<"
prop        ::= "size" | "width" | "height" | "n_colors" | "n_holes"
              | "hole_size" | "color"

action      ::= "fill(" expr_c ")" | "fill_holes(" expr_c ")"
              | "outline(" expr_c ")" | "delete()"
              | "recolor_by(" prop ("," entier "->" couleur)+ ")"
              | "move(" dir "," arret ")"
              | "move_toward(" cible ")"
              | "bar(" dir "," expr_c "," expr_n ")"
              | "rays(" mode_rayon "," expr_c ")"
              | "complete_pattern()" | "crop_to_selection()"
globale     ::= "fill_lines(" axe "," couleur ")"

dir         ::= "up" | "down" | "left" | "right"
arret       ::= "edge" | "contact" | entier
cible       ::= pred                      (objets NON sélectionnés matchant pred)
mode_rayon  ::= "open_corner" | "corners_out"
axe         ::= "rows" | "cols" | "both"
expr_c      ::= couleur | "own_color" | "minor_color" | "major_color"
expr_n      ::= entier | "size" | "n_colors" | "n_holes" | "width" | "height"
couleur     ::= 0..9      entier ::= 1..30
```

Une ligne = un programme (format proposeur/vérifieur inchangé). La référence
donnée au prompt sera générée depuis le code (`dsl_reference()`), comme en v1.

## 5. Sémantique des primitives nouvelles

Comptage : **15 nouvelles** — 2 segmentations, 1 filtre, 11 actions, 1 globale.

| # | primitive | sémantique |
|---|---|---|
| 1 | `objects(conn[,multi])` | segmente les cellules non-fond (§3.3) ; sélection initiale = tous les objets |
| 2 | `regions()` | segmente les cellules de fond en régions 4-connexes |
| 3 | `keep(pred)` | réduit la sélection aux objets satisfaisant `pred` ; sélection vide = grille inchangée à l'action |
| 4 | `fill(expr_c)` | recolore toutes les cellules des objets sélectionnés |
| 5 | `fill_holes(expr_c)` | colorie les cellules de fond encloses dans chaque objet sélectionné (masque enclos de la v1, calculé par bbox d'objet) |
| 6 | `outline(expr_c)` | trace le périmètre de la bbox élargie d'1 cellule, uniquement sur le fond, rogné aux bords |
| 7 | `delete()` | remplace les objets sélectionnés par le fond |
| 8 | `recolor_by(prop, v->c, …)` | recolore chaque objet selon la valeur de sa propriété via la table ; valeur absente de la table = objet inchangé |
| 9 | `move(dir, arret)` | translate chaque objet d'1 cellule à la fois : `edge` = jusqu'au bord, `contact` = jusqu'à 8-adjacence avec une cellule non-fond hors objet, `n` = n pas |
| 10 | `move_toward(cible)` | pour chaque objet sélectionné : direction (axe dominant du vecteur entre centres de bbox, égalité → vertical) vers l'objet cible le plus proche parmi les non-sélectionnés matchant `cible`, avance jusqu'au contact (8-adjacence) |
| 11 | `bar(dir, expr_c, expr_n)` | accole à la bbox de chaque objet, côté `dir`, un rectangle plein de couleur `expr_c`, de longueur `expr_n` dans la direction et de largeur = côté correspondant de la bbox |
| 12 | `rays(mode, expr_c)` | `open_corner` : depuis le coin manquant de la bbox de chaque objet (unique cellule de fond de la bbox), rayon diagonal fuyant l'objet ; `corners_out` : depuis chaque coin de bbox, rayon diagonal vers l'extérieur ; tracé sur fond uniquement, rogné aux bords |
| 13 | `complete_pattern()` | mode `multi` requis ; gabarit = plus grand objet ; pour chaque objet mono-cellule dont la couleur apparaît dans le gabarit, colle le gabarit en alignant cette cellule sur la cellule correspondante (si plusieurs correspondances : la première en ordre canonique interne au gabarit) ; écrit sur fond uniquement |
| 14 | `crop_to_selection()` | rogne la grille à la bbox englobante des objets sélectionnés (généralise `crop_to_content` aux sélections) |
| 15 | `fill_lines(axe, c)` | globale (hors bloc objet) : toute ligne/colonne entièrement monochrome de la couleur du fond est recolorée en `c` |

Expressions par objet : `own_color` (couleur de l'objet ; en `multi`, sa couleur
majoritaire), `minor_color` / `major_color` (couleur non-fond la moins / la plus
fréquente de la grille), et pour `expr_n` les propriétés entières de l'objet.
`hole_size` = nombre total de cellules encloses ; `n_holes` = nombre de
composantes encloses ; `unique_shape` / `unique_color` = objets dont la forme
normalisée (translation + couleur effacée) / la couleur n'apparaît qu'une fois.

## 6. Dix programmes exemples sur tâches dev réelles

Programmes **candidats**, écrits sur lecture des paires train ; leur
vérification exécutable sur tout le train est l'objet du palier 1. Tâches 1-9 :
liste gelée des 26 ; tâche 10 : near-miss X-64.

| # | tâche (dev) | règle observée | programme v2 |
|---|---|---|---|
| 1 | `00d62c1b` | les trous des formes vertes deviennent jaunes | `objects(4) \| fill_holes(4)` |
| 2 | `6455b5f5` | murs (2) découpent le fond ; plus grande pièce → 1, plus petite(s) → 8 | `regions() \| keep(largest) \| fill(1) \| regions() \| keep(smallest) \| fill(8)` |
| 3 | `b27ca6d3` | les paires de cellules 2 adjacentes sont encadrées en 3 | `objects(8) \| keep(size >= 2) \| outline(3)` |
| 4 | `05f2a901` | l'objet rouge glisse jusqu'au contact de l'objet azur | `objects(4) \| keep(color == 2) \| move_toward(color == 8)` |
| 5 | `3e980e27` | chaque point isolé est complété en copie du motif contenant sa couleur | `objects(8, multi) \| complete_pattern()` |
| 6 | `fcc82909` | sous chaque objet, un bloc 3 de hauteur = nb de couleurs de l'objet | `objects(8, multi) \| bar(down, 3, n_colors)` |
| 7 | `c1d99e64` | les lignes/colonnes entièrement fond sont tracées en 2 | `fill_lines(both, 2)` |
| 8 | `6e19193c` | chaque L de 3 cellules tire un rayon diagonal par son coin ouvert | `objects(4) \| rays(open_corner, own_color)` |
| 9 | `ec883f72` | rayons diagonaux depuis les coins du grand rectangle, couleur de l'objet mineur | `objects(4, multi) \| keep(largest) \| rays(corners_out, minor_color)` |
| 10 | `f25fbde4` | rogner au contenu puis agrandir ×2 (programme v1 conservé) | `crop_to_content \| scale(2)` |

Lecture : les exemples 4, 5, 6, 8 et 9 sont **inexprimables en v1** quel que
soit le nombre de compositions — chacun exige un paramètre calculé (direction,
gabarit, hauteur, coin, couleur). C'est exactement la classe désignée par les
999 rejets train de X-64.

## 7. Couverture attendue de la taxonomie (a priori, à mesurer au palier 1)

| famille (26 gelées + near-miss) | couverte par | tâches visées |
|---|---|---|
| remplissage de trous / pièces | `fill_holes`, `regions`+`fill`, `recolor_by` | `00d62c1b`, `6455b5f5`, `44d8ac46`, `7447852a`, `4c5c2cf0`… |
| tracés calculés (rayons, lignes, cadres) | `rays`, `fill_lines`, `outline`, `bar` | `6e19193c`, `ec883f72`, `c1d99e64`, `2bee17df`, `b27ca6d3`, `fcc82909` |
| motifs propagés | `complete_pattern` | `3e980e27`, et à évaluer `045e512c`, `57aa92db` |
| déplacements relatifs | `move`, `move_toward` | `05f2a901`, `025d127b` (hors liste) |
| hors de portée v2 assumé | — | `28e73c20` (spirale), `f15e1fac` (rayons brisés), `f35d900a`, `d9f24cd1` (trajectoires avec obstacles) |

L'aveu « hors de portée » est volontaire : le critère de falsification se joue
sur le dev complet, pas sur la saturation des 26.

## 8. Hypothèse et critère de falsification (repris du ticket, à valider par Reda)

- **Hypothèse** : une DSL v2 objectale d'au plus ~15 primitives supplémentaires
  permet d'exprimer (programme écrit à la main, vérifié par l'interpréteur sur
  tout le train) **≥ 40 des 200 tâches dev (20 %)**, dont **≥ 10 des 26
  `fill_background` gelées**.
- **Falsification** : si, après spécification complète et écriture manuelle des
  programmes, **< 30/200 tâches dev (15 %)** sont exprimables, la DSL objectale
  telle que spécifiée ne comble pas l'écart — retour à la table à dessin avant
  tout run LLM.

Cette spécification ne modifie ni les seuils ni la méthode de comptage. Une
tâche compte « exprimable » si un programme v2 écrit à la main reproduit
exactement **toutes** les paires train ET les paires test de la tâche dev
(le test dev n'est pas le split final ; il évite de compter des programmes
sur-ajustés au train). Coût : 0 $ — aucun appel API aux paliers 0 et 1.

## 9. Plan du palier 1 (après go explicite de Reda)

1. Interpréteur : `solveur/dsl/objects.py` (segmentation, propriétés, rendu) +
   extension de `parse.py` (grammaire §4, erreurs motivées) ; `dsl_reference()`
   étendu, générée depuis le code, jamais divergente de l'interpréteur.
2. Tests (mocks, aucun réseau) : un test par primitive sur grilles synthétiques,
   les cas de départage du §3.4, non-régression v1 complète (les 12 primitives
   et le brute-force intacts), verrou `FinalSetLockedError` intouché.
3. Étude d'expressivité manuelle sur les 200 tâches dev : programmes écrits à la
   main, vérifiés par l'interpréteur, rapport `reports/dsl_v2_expressivite.md`
   (tâches exprimables, programmes, comptage vs seuils §8 — le chiffre qui
   décide de l'EPIC-2).

## 10. Points ouverts pour la revue

1. `move_toward` : la règle « axe dominant, égalité → vertical » est un choix ;
   alternative : trajectoire diagonale autorisée. Trancher avant le palier 1.
2. `complete_pattern` : gabarit = plus grand objet — suffisant sur `3e980e27`,
   mais un mode « gabarit par couleur d'ancre » pourrait couvrir plus large.
3. `fill_lines` traite la couleur de fond ; variante « ligne monochrome de
   n'importe quelle couleur » si des tâches dev l'exigent.
4. Faut-il un `keep(rank_size == i)` général ou `largest`/`smallest` suffisent ?
   (Inclus dans la grammaire, coût nul en surface de prompt — à confirmer.)
