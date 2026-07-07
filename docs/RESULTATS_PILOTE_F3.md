> **Note d'intégration (2026-07-06, v2)** : étude complémentaire externe transmise par
> Reda en deux livraisons, intégrée après vérification d'alignement (voir
> `preuves_invariance.md` v0.3, journal de réconciliation). Code : `experiments/pilote_f3/`.
> La v2 ajoute le §9 (registre intermédiaire recettes, **prédiction pré-enregistrée au
> §8 de la v1 avant de voir les données**) et un correctif de classifieur (fractions vs
> dates — vérifié dans le diff du code : les corpus v1 restent stables, lift P2b 58→59×).
> **Ré-exécution locale FAITE (2026-07-07, campagne F3, H-R du pré-enregistrement)** :
> corpus retéléchargés des dépôts officiels, `resultats.json` régénéré (run v2, dans les
> tolérances pré-déclarées : A e-SNLI 0,22 % (43), LIAR 21,96 %, lift P2b 59,1×, recettes
> 48,7 %/22,8 %). Statut : PILOTE — ne remplace pas le F3 du noyau (garde-fou A-G23) ;
> campagne humaine pré-enregistrée dans `PREREGISTREMENT_F3.md`, paquet juges dans
> `experiments/f3/`.

# Pilote F3 — « la langue parle en invariants » face à trois corpus réels

**Statut** : pilote (classifieur à règles + audit manuel par un seul juge). Il ne
remplace PAS le F3 du noyau (juges humains indépendants) ; il teste si la
conjecture SURVIT à un premier contact avec des données réelles, à coût quasi nul.
**Verdict court : elle survit, nettement, sur les deux prédictions.**

## 1. Objet

Tester [Déf 2.3] version faible, reformulée via la grammaire I1 v0.2
(quatre classes, cf. PREUVES_v0.2.md §4) :
- **(P1)** dans les registres explicatifs, la part de clauses contenant une
  constante d'axe (classe A) est très faible ; I + C + N dominent ;
- **(P2a)** inter-registres : les registres de calibration (vérification
  factuelle) regorgent de A ;
- **(P2b)** intra-registre : dans un corpus explicatif, A n'apparaît quasiment
  que lorsque l'explanandum contient lui-même une constante à calibrer.

## 2. Données (réelles, publiques)

| Corpus | Nature | Unités analysées |
|---|---|---|
| **e-SNLI** (Camburu et al. 2018) | Explications libres écrites par des humains pour justifier des jugements d'implication (prémisse = légende d'image, hypothèse) | 19 666 explications (dev + test, Explanation_1) |
| **CoS-E v1.11** (Rajani et al. 2019) | Explications libres pour du QA de sens commun (corpus réputé bruité) | 1 213 explications (dev) |
| **LIAR-PLUS** (Alhindi et al. 2018, sur LIAR, Wang 2017) | Justifications de fact-checking PolitiFact — le registre de **calibration** par excellence | 9 941 phrases (val + test) |

## 3. Méthode

Classifieur **déterministe à règles** (`i1_classifier.py`) : lexiques fermés +
motifs. Choix délibéré : le classifieur EST l'opérationnalisation de la
grammaire, pas un modèle à valider séparément. Multi-étiquettes au niveau
phrase ; IC de Wilson à 95 % ; graine fixée.

Classes : **A** (monnaie, %, dates/heures, mesures avec unité, âges chiffrés),
**I** (comparatifs, superlatifs, équatifs, ordre temporel, identité/différence,
taxonomie « is a », implication, quantificateurs exacts), **C** (graduables en
forme positive, quantités vagues, approximation/similarité, déictiques),
**N** (numéraux de comptage — invariants, cf. PREUVES v0.2 §4).

**Audit manuel** (~90 phrases lues, tirage aléatoire stratifié) → deux correctifs
appliqués AVANT la passe finale, tous deux justifiés théoriquement et non par le
résultat : (1) « foot/feet » compté comme unité seulement s'il est suivi d'un
marqueur de mesure (of/tall/deep/…) — sinon c'est la partie du corps (« standing
on one foot » : 4 faux positifs sur 15 dans l'échantillon A d'e-SNLI) ;
(2) « infer » ajouté au vocabulaire d'implication (omniprésent dans e-SNLI).
Effet des correctifs : A d'e-SNLI 0,26 % → 0,21 % (le résultat pré-correctif
était donc déjà conservateur dans le sens de l'hypothèse).

## 4. Résultats

### Taux de présence par phrase (IC de Wilson 95 %)

| Classe | e-SNLI (n=19 666) | CoS-E (n=1 213) | LIAR-PLUS (n=9 941) |
|---|---|---|---|
| **A — constante d'axe** | **0,21 %** [0,16–0,29] (42) | **0,41 %** [0,18–0,96] (5) | **22,0 %** [21,2–22,8] (2 188) |
| I — invariant explicite | 58,0 % [57,3–58,7] | 23,7 % [21,4–26,2] | 44,5 % [43,6–45,5] |
| C — calibré-contexte | 15,8 % [15,3–16,4] | 14,3 % [12,4–16,3] | 29,7 % [28,8–30,6] |
| N — cardinalité | 12,9 % [12,4–13,4] | 1,6 % [1,0–2,4] | 25,0 % [24,2–25,9] |

Composition exclusive (priorité A>I>C>N>OTHER), e-SNLI : A 0,2 / I 57,9 /
C 6,1 / N 4,3 / OTHER 31,5 %. LIAR : A 22,0 / I 32,8 / C 12,3 / N 4,3 /
OTHER 28,6 %. L'OTHER d'e-SNLI est, à l'audit, de la prédication catégorielle
nue (« A field of flowers is outside ») — invariante au sens large mais sans
marqueur relationnel explicite ; décision de comptage conservatrice.

### P1 — dominance du fragment sans constante

99,8 % des phrases explicatives d'e-SNLI (99,6 % de CoS-E) ne contiennent
**aucune** constante d'axe. Ce chiffre n'est PAS tautologique : le même
instrument mesure 22,0 % dans LIAR-PLUS — la mesure a une dynamique de deux
ordres de grandeur, et le registre explicatif choisit le bas de cette dynamique.
**P1 : soutenu.**

### P2a — concentration inter-registres

Ratio LIAR / e-SNLI sur la classe A : **× 103** (22,0 % vs 0,21 %). Le registre
adossé à l'infrastructure métrologique (dates, dollars, pourcentages : les
sous-marqueurs A dominants de LIAR sont A:measure 1 028 et A:date 976) est bien
celui qui sort du fragment. **P2a : soutenu.**

### P2b — concentration intra-registre (le test le plus fin)

Dans e-SNLI, P(A dans l'explication | numéral dans prémisse∪hypothèse) =
**0,79 %** [0,58–1,07] (40/5 067) contre **0,014 %** [0,004–0,050] (2/14 599)
sinon : **lift × 58**. Autrement dit, 40 des 42 explications contenant une
constante d'axe répondent à un explanandum qui en contenait une — l'absolu
n'apparaît dans l'explication que pour **relier une constante donnée à un
concept** (23,8 % des phrases A ont explicitement la forme-calibration
« NUM … copule … graduable/catégorie », p. ex. *« A man can be an age other than
20 years old »*, *« An old man must be more than fifteen years old »* — des
énoncés de calibration au sens strict de W_cal). Contrôle : le lift de N
(comptes recopiés de l'input) n'est que × 5,9 — la concentration de A n'est pas
un simple artefact de recopie. **P2b : soutenu.**

### La bifurcation des numéraux, vindiquée

e-SNLI : N = 12,9 % vs A = 0,21 %. Les numéraux d'un registre perceptif sont
massivement des **comptes** (invariants), presque jamais des mesures. Si la
grammaire v0.1 (binaire) avait compté tout numéral comme « absolu », elle aurait
conclu à ~13 % de sorties du fragment — la classe N n'est pas un raffinement
cosmétique, elle change la conclusion d'un facteur ~60.

## 5. Audit de précision (lecture manuelle, un juge)

Classe A e-SNLI : 11/15 avant correctifs (4 FP « one foot »), patrons corrigés.
Classe A LIAR : 15/15. Classe I e-SNLI : 15/15. Classe C : ~13/15 (bruit :
composés lexicalisés type « high heels »). OTHER (30 lues) : aucun A manqué.
Le rappel de A est vraisemblablement élevé (patrons quasi clos : symboles
monétaires, %, années, unités) ; le rappel de I/C n'est pas mesuré — c'est le
travail du F3 propre.

## 6. Lecture théorique

1. La structure interne du fragment dans e-SNLI est celle que le noyau ℛ
   prédit : implication/inclusion 27,7 % des phrases, taxonomie 12,3 %,
   identité 9,8 %, quantification exacte 9,4 %, ordre 7,4 %, comparatif 3,4 %.
   La langue explicative parle en relations d'ordre, d'inclusion et
   d'implication — pas en coordonnées.
2. C = 15,8 % : le royaume de W_cal est substantiel et distinct — exactement la
   classe que Kennedy (2007) isole. Le binaire v0.1 l'aurait perdue.
3. Métrologie (Rem. 4.2 des preuves) : les A de LIAR sont portés par dates,
   monnaies et pourcentages — les trois grandes infrastructures de calibration
   sociale. Cohérent avec « A = ce qui exige un canal pré-calibré ».

## 7. Ce qui aurait falsifié — et limites

Aurait falsifié : A élevé dans e-SNLI/CoS-E ; absence de dynamique (LIAR ≈
e-SNLI) ; lift intra-corpus ≈ 1. Rien de tout cela ne s'est produit.

Limites, sans complaisance : anglais uniquement ; unité = phrase, pas clause ;
un seul juge (l'audit mesure la précision, pas le rappel de I/C) ; e-SNLI est un
registre perceptif concret (favorable) ; les justifications LIAR-PLUS sont de la
prose éditoriale extraite, pas des explications adressées à un récepteur ;
CoS-E est bruité (connu). Le F3 du noyau reste requis : 200–500 clauses,
≥ 2 juges humains indépendants, accord inter-juges, corpus français inclus.

## 8. Prochaines étapes proposées

(1) Protocole d'annotation humaine à 4 classes + guide (les cas limites de
l'audit en sont l'ébauche : composés lexicalisés, déictiques, numéraux). 
(2) Repasse française — adapter les lexiques ; les corpus de Reda bienvenus.
(3) Registre intermédiaire prédictif : notices techniques / recettes —
prédiction : A concentré dans les quantités (les recettes sont des suites de
calibrations), I domine les étapes.

## Reproduction

`python3 run_pilote.py` (données : `data/`, téléchargées des dépôts GitHub
officiels ; classifieur : `i1_classifier.py` ; sortie : `resultats.json`,
`samples_audit.txt`).

---

## 9. Addendum — le registre intermédiaire (recettes), prédiction pré-enregistrée

Corpus réel : **based.cooking** (350 recettes anglophones, markdown structuré),
sections Ingrédients / Étapes séparées. La prédiction du §8 était écrite AVANT de
voir les données : « A concentré dans les quantités ; I domine l'enchaînement des
étapes ». Un correctif de classifieur a été nécessaire et appliqué avant lecture
finale : les fractions « 1/2 » étaient happées par le motif de date à barres
(désormais, une date à barres exige trois composantes j/m/aa) ; les corpus du §4
restent stables après correctif (e-SNLI 0,2 % ; LIAR 22,0 % ; lift P2b 59×).

| Classe | Ingrédients (n=2 571) | Étapes (n=3 544) |
|---|---|---|
| **A — constante d'axe** | **48,7 %** [46,7–50,6] | **22,8 %** [21,5–24,2] |
| N — cardinalité | 31,4 % | 10,3 % |
| I — invariant explicite | 4,5 % | 34,0 % (dont ordre : 20,8 %) |
| C — calibré-contexte | 12,1 % | 31,4 % |

Lecture :
1. **Gradient dans le sens prédit** (A : ×2,1 ingrédients/étapes), et le registre
   est globalement dense en calibration — cohérent avec Rem. 4.2 : la cuisine a sa
   propre infrastructure métrologique (tasses, cuillères, degrés).
2. La **bifurcation des numéraux** est photographiée : une ligne d'ingrédient est
   soit une mesure (« 270 g de farine » → A, 99,8 % des A d'ingrédients sont
   A:measure), soit un compte (« 2 œufs » → N, 31,4 %).
3. Les A des étapes sont à **99,5 % des temps et des températures** — des
   calibrations locales insérées dans une ossature qui, elle, est faite d'ordre
   (until/then/before : 20,8 %) et de graduables contextuels (31,4 %). « Cuire
   *jusqu'à ce que* ce soit *doré* » est littéralement : itérer le processus
   jusqu'au franchissement du standard contextuel d'un prédicat graduable — une
   boucle W_cal à l'impératif.
4. Les quatre registres forment maintenant un **spectre de densité de
   calibration** : explications 0,2 % → étapes de recettes 22,8 % ≈ fact-check
   22,0 % → lignes d'ingrédients 48,7 %. A n'est pas une constante de la langue,
   c'est une variable de registre indexée sur la calibration — exactement la
   forme de [Déf 2.3] version faible.
