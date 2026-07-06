# I1 — Grammaire du fragment invariant = spécification du noyau ℛ (v0.2)

**Statut** : livrable de l'issue X-43, version 0.2 — fusion de la grammaire à quatre
classes de l'étude complémentaire (reçue le 2026-07-06, validée par pilote sur trois
corpus réels) et du critère sémantique issu de notre relecture adverse (L2). Fondée sur
T2/(H) (`preuves_invariance.md`) : le fragment invariant est mathématiquement caractérisé,
la grammaire le découpe là où le théorème l'impose.

## 1. Les quatre classes (annotation multi-étiquettes par clause)

**I — fragment invariant explicite.** Comparatifs, équatifs, superlatifs et rangs ;
ordre temporel (avant/après/pendant — précédences d'Allen) ; entre-deux ; identité et
différence qualitatives ; inclusion taxonomique (« X est un Y »), implication et son
refus ; quantificateurs exacts (tous, aucun, chaque, la moitié, la majorité).
Sémantique : les atomes de T2 (iii), plus les prédications de concepts nommés sans
constante.

**C — calibré par le contexte.** Graduables en forme positive (« il est grand ») —
standard θ(κ) fourni par la classe de comparaison (Klein 1980 ; Kennedy 2007) ;
quantités vagues (beaucoup, peu, plusieurs) ; approximation/similarité (≈_κ, résolution
ε_κ, [Déf 9.1] du noyau) ; déictiques temporels (aujourd'hui, hier — indexicaux calibrés
par la situation). Formellement : des invariants CONDITIONNELS — invariants dès que κ
fournit le standard. **C est le domaine naturel de W_cal.**

**A — constante d'axe (la vraie sortie du fragment).** Valeur numérique sur un axe de
qualité ordonné : monnaie, pourcentage, date, heure, mesure avec unité, âge chiffré.

**N — cardinalité (DANS le fragment).** Numéral comptant des OBJETS (« deux hommes »).
Découverte de la relecture de l'étude : G agit sur les axes de qualités, pas sur le
multi-ensemble des objets — le cardinal d'une configuration est préservé par tout
g ∈ G. **Les numéraux bifurquent** : compte (invariant) vs mesure (absolu). Le pilote
montre que cette bifurcation change la conclusion d'un facteur ~60 sur e-SNLI
(N = 12,9 % vs A = 0,21 %).

## 2. Le critère de classe A, précisé (notre L2 — obligatoire avant annotation)

Un énoncé sort du fragment **ssi sa valeur de vérité dépend effectivement de la
constante** (critère sémantique). Conséquences opérationnelles :
- les tautologies/contradictions à constantes (« x ≥ 12 000 ∨ x < 12 000 ») restent
  invariantes — ne pas les compter en A ;
- les constantes ÉLIMINABLES (reformulables en énoncé d'ordre inter-objets) ne comptent
  pas en A ;
- le classifieur opérationnel est syntaxique : déclarer AVANT l'annotation la liste
  d'exceptions (tautologies, redondances, constantes éliminables) et les compter à
  l'audit. Cas limites documentés par le pilote : composés lexicalisés (« high heels »),
  déictiques, numéraux (« one » pronominal vs comptage), parties du corps homonymes
  d'unités (« foot »).

## 3. Deux remarques structurantes (adoptées de l'étude)

**Métrologie = W_cal institutionnalisé.** Les énoncés A ne circulent que parce qu'une
infrastructure sociale coûteuse (unités SI, monnaies, calendriers) a pré-calibré le
canal une fois pour toutes. Prédiction dérivée, testée positivement par le pilote : A se
concentre dans les registres adossés à cette infrastructure (fact-checking : 22,0 % vs
0,21 % en registre explicatif — ratio ×103).

**Les adjectifs « absolus » de Kennedy = notre limite L3.** Kennedy distingue graduables
relatifs (standard contextuel → classe C) et absolus (plein, vide, sec : standard
d'extrémité d'échelle). Ces derniers sont exactement les invariants d'extrémalité de
L3 : ils existent ssi l'échelle a des bornes fixées par les automorphismes. La typologie
linguistique et la limite mathématique sont le même objet — et c'est le candidat propre
d'arité 1 (A-G15), confirmé par une seconde voie indépendante (profil de support, T3).

## 4. La conjecture, reformulée testable ([Déf 2.3] version faible → P1/P2)

- **(P1)** Dans les registres explicatifs, la part de clauses contenant une constante
  d'axe (A) est très faible ; I + C + N dominent.
- **(P2a)** Inter-registres : les registres de vérification factuelle regorgent de A.
- **(P2b)** Intra-registre : A n'apparaît quasiment que lorsque l'explanandum contient
  lui-même une constante à relier à un concept (l'énoncé de calibration au sens strict
  de W_cal : « 13 personnes, c'est un grand groupe »).

État empirique (pilote, trois corpus réels — voir `RESULTATS_PILOTE_F3.md`) : P1, P2a,
P2b soutenus (A = 0,21 % en e-SNLI ; ratio inter-registres ×103 ; lift intra-registre
×58). **Statut : pilote — un juge, anglais seul, non pré-enregistré ; ne remplace pas
F3.**

## 5. Ce qui reste pour clore F3 (le vrai)

1. Guide d'annotation humaine à 4 classes (les cas limites du §2 en sont l'ébauche).
2. 200-500 clauses, ≥ 2 juges humains indépendants, accord inter-juges rapporté.
3. Corpus français inclus (adapter les lexiques) ; registre intermédiaire prédictif
   (notices/recettes : A concentré dans les quantités, I dans les étapes).
4. Pré-enregistrement (hypothèses P1/P2, seuils de falsification) AVANT l'annotation.
