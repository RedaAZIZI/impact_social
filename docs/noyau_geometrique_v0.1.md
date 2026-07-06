# Noyau géométrique v0.1 — formes, invariants, contexte

**Périmètre** : modélisation mathématique de la nouvelle direction (FONDAMENTAUX sessions
5-8, décision STRATEGIE du 2026-07-06). Prolonge le noyau formel v0.1 (mêmes notations :
V_R, Expl_D, W, W⁻¹, θ) — ne le remplace pas. Objectif : identifier les **faits
nécessaires** (§6) dont la vérité conditionne le go définitif de la direction.

**Statut des énoncés** : [T] théorème (preuve esquissée) · [P] proposition ·
[C] conjecture / chantier · [Déf] définition · [F] fait nécessaire (go/no-go).

---

## 1. La géométrie ordinale (ce qui est déjà démontré, dit proprement)

**[Déf 1.1] (espace des qualités).** X = ∏_{i=1..d} X_i où chaque (X_i, ≤_i) est un
ensemble totalement ordonné (dimension de qualité NOMMÉE). Aucune structure métrique
n'est supposée. C'est délibéré : tout ce qui suit doit tenir sans distances.

**[Déf 1.2] (le groupe).** G := ∏_i Mon(X_i), produit des homéomorphismes strictement
croissants coordonnée-par-coordonnée. Au sens du programme d'Erlangen (Klein 1872), le
couple (X, G) EST une géométrie : la **géométrie ordinale produit**. Ce qui la
caractérise : G préserve les ordres par axe, les inclusions de boîtes, les précédences —
et ne préserve ni valeurs absolues, ni distances, ni angles.

**[Déf 1.3] (forme / concept).** Un concept est une région nommée C ⊆ X prise dans une
famille contrainte close sous G :
- **boîtes** : ∏_i [a_i, b_i] (les règles actuelles de /core) ;
- **unions finies de boîtes** (concepts disjonctifs — hors critère P de Gärdenfors,
  assumé) ;
- **superpositions** : mesures sur des boîtes à squelette partagé (les
  seuils-intervalles de la session 2 ; μ_C(x) = fraction de la superposition contenant x).
La contrainte de nommabilité (garde-fou A-G2) : chaque face d'une forme est un prédicat
sur une dimension nommée ; ajouter une direction composée nommée (ex. « ratio
dette/revenu ») = étendre l'atlas, pas apprendre une surface libre.

**[P 1.4] (Prop 1 en langage de groupe).** Pour tout g ∈ G, tout modèle M et tout
récepteur R à vocabulaire de seuils sur les axes : Expl_D(M, R, ε) =
Expl_{g·D}(M∘g⁻¹, R∘g⁻¹, ε). *Esquisse.* Un graphe à seuils est entièrement déterminé
par les rangs des seuils parmi les valeurs des données sur chaque axe ; g préserve tous
les rangs ; la bijection G ↦ g·G entre graphes préserve taille et fidélité. ∎(esquisse)
C'est l'Exp 1b (11 runs sur 11, écart souvent exactement 0.0000) élevée au rang
d'énoncé : **le coût d'explicabilité est un invariant de la géométrie ordinale.**

**[C 1.5] (le coût du mélange).** Les transformations HORS de G (mélanges, rotations)
portent tout le coût : Expl croît avec les angles principaux entre le repère intrinsèque
B*_M et le repère de R (reprend [C 4.3] du noyau v0.1 — loi sin(2θ) en 2D, forme
multi-axes à établir).

## 2. Le fragment invariant (la conjecture, formalisée)

**[Déf 2.1] (énoncé invariant).** Un énoncé φ sur X (à valeurs booléennes ou ordinales)
est invariant si φ(g·x_1, …, g·x_n) = φ(x_1, …, x_n) pour tout g ∈ G. Exemples :
« x plus grand que y sur l'axe i » (comparatif) ; « C ⊆ C′ » (inclusion, donc
implication) ; « intervalle I avant J sur l'axe temps » (précédence, Allen) ;
qualificatifs monotones (« très » = plus loin dans l'ordre). Contre-exemples :
« x_i = 12 000 » ; « à distance 3 de » ; toute valeur absolue, unité, seuil chiffré.

**[C 2.2] (caractérisation — LA cible théorique du programme I).** Les énoncés
invariants de la géométrie ordinale produit sont exactement les combinaisons booléennes
de comparaisons d'ordre par axe (et des relations qui s'en déduisent : inclusions de
boîtes, précédences, dominances par projection). *Piste : structure d'automorphismes
riche de G — deux configurations de même type d'ordre sont dans la même orbite ; un
invariant ne peut dépendre que du type d'ordre.* Si [C 2.2] tombe (des invariants
exotiques existent), la grammaire I1 est mal posée — voir [F1].

**[Déf 2.3] (la conjecture « la langue parle en invariants »).** Version faible
(distributionnelle, testable — programme I) : dans les explications humaines, la
fraction d'énoncés appartenant au fragment invariant domine massivement, et les sorties
du fragment (absolus) se concentrent aux moments de calibration. Version forte
(fonctionnelle, hors périmètre expérimental direct) : cette dominance existe PARCE QUE
chaque locuteur tient une base déformée par un g ∈ G inconnu de l'autre — le fragment
invariant est le seul code décodable sans estimation du canal.

## 3. Le canal (session 8, formalisé a minima)

**[Déf 3.1] (canal de langue).** Émetteur S et récepteur R partagent les NOMS des
dimensions mais pas leurs calibrations : il existe g_SR ∈ G inconnu tel que la lecture
de R soit x ↦ g_SR(x). Un message m est décodable sans estimation si sa valeur de vérité
chez R égale celle chez S pour TOUT g_SR — c'est-à-dire ssi m est dans le fragment
invariant ([Déf 2.1]). Les énoncés absolus exigent d'estimer g_SR.

**[P 3.2] (pilotes — complexité de calibration, un axe).** Estimer la composante
g_i ∈ Mon(X_i) au voisinage d'un seuil à précision δ demande Θ(log 1/δ) requêtes de
calibration par bissection (E1, session 3). W_cal = le symbole pilote du canal.
[C 3.2b] Version multi-axes et version « réponses grossières » (μ rendu sur 3-5
niveaux) : à établir — c'est le test de robustesse qui décide si W_cal mérite le statut
d'opérateur primitif (E1, session 3).

**[P 3.3] (lecture débit-distorsion).** Les courbes F_{M,R}(k) du noyau v0.1 sont des
courbes débit-distorsion du canal (budget k = débit, 1 − fid = distorsion) ; le
désalignement hors-G réduit la capacité effective (Exp 1 = mesure de perte de capacité ;
plafond de l'Exp 2 = capacité finie, dérivée par C3 du noyau v0.1). Aucun calcul
nouveau : relecture.

## 4. Le contexte (l'exigence centrale de Reda : « le contexte définit la géométrie et
l'existence des objets »)

Trois formalisations candidates, ordonnées par engagement ontologique croissant. La
discipline : monter d'un cran SEULEMENT quand une mesure force le cran supérieur.

**[Déf 4.1] (K1 — contexte comme section).** κ = (S_κ, π_κ, Q̄_κ) : sous-espace actif,
projection nommée, distribution de questions. Le contexte choisit LA PROJECTION sous
laquelle les comparatifs se lisent (« plus grand » : en hauteur ou en volume ?). Rend
compte : dépendance à Q (Exp 4), fork des calibrations (E3), lecture géométrique de A3
faible. Ne touche ni aux concepts ni à leur existence.

**[Déf 4.2] (K2 — contexte comme saillance).** κ = w_κ : X → poids par dimension
(saillance, Gärdenfors ch. contextuel). Remarque cruciale : une repondération par axe
est DANS G (c'est une déformation monotone coordonnée-par-coordonnée) — le contexte au
sens K2 change la saillance SANS casser la géométrie, et [P 1.4] prédit qu'il ne change
pas le coût d'explicabilité. Prédiction contre-intuitive et testable.

**[Déf 4.3] (K3 — contexte comme fibre : la lecture forte).** Les contextes forment une
catégorie K (morphismes = raffinements/changements de contexte). L'espace des qualités
est fibré p : E → K ; un concept est une SECTION locale c : U ⊆ K → E (sa forme varie
avec le contexte) ; le vocabulaire lui-même est un préfaisceau V : K^op → Set. **« Le
contexte définit l'existence des objets » = V(κ) peut être vide ou lacunaire : un
concept n'existe qu'au-dessus de certains contextes.** Les applications de restriction
V(κ→κ′) disent comment un concept se transporte. A3 forte = « V n'est pas un préfaisceau
constant ». Test décisif hérité de la session 1 : exhiber un cas où le changement de
contexte change LES CONCEPTS DISPONIBLES, pas les questions.

**[Déf 4.4] (entraînement avec le contexte).** Données = triplets (κ, x, y). Apprendre
un concept = apprendre une section : sa forme dans chaque contexte rencontré + son
transport le long des restrictions. Le few-shot a deux sources : la convexité des formes
(Gärdenfors — dans chaque fibre) et le transport (entre fibres : seul le delta
contextuel est à apprendre). [C 4.5] Borne d'échantillon : apprendre un concept dans un
contexte nouveau κ′ coûte O(complexité du delta de restriction), pas O(complexité de la
forme) — la formalisation du « very little data ».

## 5. Où le riemannien entrerait (et pourquoi pas encore)

Deux portes d'entrée honnêtes, aucune franchie : (a) si la similarité perçue intra-
dimension exige une métrique non réductible aux ordres ; (b) si le transport contextuel
(K3) exige une connexion (comparer des formes entre fibres voisines = transport
parallèle). Règle : « riemannien » n'entre dans aucun énoncé tant qu'aucune mesure
n'exige (a) ou (b). La géométrie démontrée est ordinale.

## 6. Les faits nécessaires [F] — ce qui doit être vrai pour confirmer la direction

**[F1] La caractérisation [C 2.2] doit tenir** (les invariants de (X, G) = le fragment
comparatif/inclusif/précédentiel). Si des invariants exotiques existent, la grammaire I1
ne découpe pas la langue au bon endroit. *Attaque : preuve par types d'ordre (orbites de
G) ; niveau : faisable, à rédiger.* — Verrou de TOUT le programme I.

**[F2] [P 1.4] doit passer de l'esquisse à la preuve** (rangs → invariance). Si un
contre-exemple existe (graphes non déterminés par les rangs), l'Exp 1b devient une
coïncidence. *Risque : faible (11/11 runs à 0.0000).*

**[F3] La grammaire I1 doit être opérationnalisable** : sur la strate 0 (corpus humain
réel), des juges indépendants (humains puis synthétiques validés) doivent classer
invariant/absolu avec un accord élevé. Si les clauses réelles sont majoritairement
inclassables, la conjecture [Déf 2.3] n'est pas mesurable. — Verrou de I2/I3.

**[F4] K1 doit suffire ou être falsifié proprement** : si le fork contextuel (E3) et la
dépendance à Q (Exp 4) se modélisent en K1/K2, on reste au cran bas ; sinon, exhiber le
cas qui force K3 (le test décisif de A3). Dans les deux issues, le contexte est modélisé
— ce qui est requis, c'est que le cran soit DÉCIDÉ par une mesure, pas par goût.

**[F5] La prédiction K2 doit être testée** (la saillance ne change pas le coût — elle
est dans G) : synthétique pur, coût nul, design direct depuis [P 1.4]. Si le coût BOUGE
sous repondération par axe, [P 1.4] ou K2 est faux — dans les deux cas on apprend.

**Critère de confirmation de la direction** : F1 + F2 prouvés, F3 positif sur strate 0,
F4 tranché par une mesure, F5 conforme. Alors la v2 a un noyau théorique complet :
géométrie (§1), langue (§2), canal (§3), contexte (§4) — et le produit a sa garantie de
maintenabilité (le fragment invariant comme API, le pilote W_cal comme calibration).

## 7. Ordre d'attaque proposé

1. **I1** = rédiger la grammaire à partir de [Déf 2.1]-[C 2.2] (document, coût nul).
2. **F2** puis **F1** (théorie pure ; F1 est le morceau ambitieux).
3. **F5** (première expérience du nouveau programme : synthétique, gratuite, et elle
   teste le noyau au lieu de l'illustrer).
4. **F3** : inventaire des corpus humains gratuits (strate 0), puis annotation.
5. **F4** : relire E3/Exp 4 en K1 ; concevoir le test décisif seulement si K1 craque.

---

## 8. Le noyau de relations (ajout session 9 — l'inversion de primauté)

**Motivation (Reda, session 9)** : définir un noyau de relations aux propriétés
géométriques, contexte = sélecteur de projection ; les mots compris par leur profil
relationnel à travers les contextes ; arborescence + découverte de chemins ; le tout
formant une base structurée requêtable. Les formes du §1 deviennent des objets DÉRIVÉS.

**[Déf 8.1] (signature relationnelle ℛ, graduée par arité).** Sur X = ∏(X_i, ≤_i),
avec contexte κ sélectionnant une projection π_κ (K1, [Déf 4.1]) :
- arité 2 : x ≤_i y (ordre par axe nommé) ; C ⊆ C′ (inclusion, donc implication) ;
  **x ≈_κ y** ssi π_κ(x) = π_κ(y) — « quelque chose COMME quelque chose » : l'égalité
  sous la projection que le contexte définit (version superposée : indistinguabilité à
  la résolution du contexte) ;
- arité 3 : **B_i(a, x, b)** — x entre a et b sur l'axe i ; B_κ(a, x, b) — entre-deux
  sous π_κ (« au milieu de », version deux bornes) ;
- arité n : **med(x_1, …, x_n)** — médiane coordonnée-par-coordonnée (« au milieu des
  gens », « la médiane ») ;
- arité 1 : ouverte (A-G15) — candidats : extrémalité sur un axe ; complexité de
  description propre (taille à ε, session 5).

**[P 8.2] (le noyau est invariant).** Toute relation de ℛ est G-invariante : ordres,
inclusions, entre-deux et médianes par axe ne dépendent que des ordres, préservés par
les déformations monotones ; ≈_κ et B_κ sont invariants dès que π_κ est une sélection
d'axes nommés. *Preuve : lecture directe des définitions.* Conséquence : **le noyau de
relations est un sous-ensemble du fragment invariant ([Déf 2.1]) — les relations
« naturelles » de l'intuition sont exactement ce que la conjecture prédit que la langue
transporte.**

**[P 8.3] (dualité formes/relations — l'inversion est gratuite).** (X, med) avec la
médiane coordonnée-par-coordonnée est une **algèbre médiane** (fait standard : les
produits de chaînes totalement ordonnées le sont). Les convexes y sont les parties
closes par entre-deux, et les boîtes du §1 sont les intervalles med-engendrés. Donc :
les formes ([Déf 1.3]) sont DÉFINISSABLES depuis ℛ — la présentation relationnelle est
plus économe, rien du §1-§7 n'est perdu. *À rédiger proprement (références : algèbres
médianes / median graphs — Birkhoff-Kiss ; Bandelt & Hedlíková).*

**[Déf 8.4] (mot = profil relationnel).** Le sens d'un mot w relativement à une
population d'objets O et une famille de contextes K : type(w) := { (φ, κ) : φ formule
sur ℛ, κ ∈ K, (w, O) ⊨_κ φ } — l'ensemble contextué des relations qu'il satisfait
(type au sens de la théorie des modèles). Apprendre un mot = remplir son profil ;
la comparaison de profils fonde la similarité lexicale SANS vecteur.

**[Déf 8.5] (arborescence et découverte de chemins).** Relations dérivées = compositions
et combinaisons booléennes de ℛ (algèbre relationnelle). L'arborescence = le treillis
des relations définissables, exploré incrémentalement. **Mécanisme de découverte** :
un chemin composé récurrent et compressif est promu en relation NOMMÉE (l'acte de
nommage de la session 4, appliqué aux relations) ; une relation dérivée non nommée ne
persiste pas (garde-fou A-G13 contre l'explosion).

**[Déf 8.6] (la base requêtable).** KB := (O, ℛ, K, faits) où les faits sont des atomes
φ(o_1, …, o_n) sous contexte. Requêter = évaluer une formule du noyau sous un contexte ;
le transducteur (FONDAMENTAUX session 4) traduit langue ↔ formules ; W lit, W⁻¹ écrit,
W_cal calibre les projections. Cible de comparaison (A-G14) : précision, éditabilité,
localité, traçabilité sur domaines bornés — pas la couverture ouverte d'un LLM.

**[F6] (complétude du noyau — raffine F1).** ℛ engendre-t-il par définissabilité tous
les invariants de (X, G) ([C 2.2]) ? Si oui, le noyau de relations et le fragment
invariant coïncident — et « la langue parle en invariants » devient « la langue parle
dans le noyau ℛ » : la conjecture linguistique et l'architecture de la KB sont le même
objet. Si non, exhiber les invariants manquants et compléter la signature. **C'est le
fait nécessaire qui soude la session 9 au reste du programme.**

### Mise à jour de l'ordre d'attaque (§7)

L'étape 1 (I1) absorbe [Déf 8.1] : la grammaire du fragment invariant s'écrit
directement comme la grammaire des formules sur ℛ — I1 et la spécification du noyau
relationnel sont UN SEUL document. F1 et F6 s'attaquent ensemble (types d'ordre ↔
définissabilité). Le reste de l'ordre est inchangé.

---

## 9. Résolution, fermeture, diagonale, dynamique (ajout session 10)

**[Déf 9.1] (résolution contextuelle — le ε appartient à κ).** Le contexte est complété :
κ = (π_κ, Q̄_κ, ε_κ) où ε_κ est un maillage fini de bandes ordonnées par axe actif (la
granularité). Version ordinale de la tolérance, sans métrique. La similarité de la
session 9 devient : **x ≈_κ y ssi π_κ(x) et π_κ(y) tombent dans les mêmes bandes de
ε_κ** — « pomme comme banane » sous π_fruit à la résolution fruit. Le ε de
Expl(M, R, Q, ε) est fourni par le contexte : la lecture faible de A3 (session 1,
κ = (Q̄, ε, sous-graphe)) est DÉRIVÉE de la géométrie, composante par composante.
Garde-fou A-G18 : ε_κ est pré-déclaré par contexte, jamais ajusté après jugement.
[C 9.1b] L'abstraction = grossissement de résolution ; la hiérarchie des concepts =
l'ordre (partiel ?) des maillages.

**[Déf 9.2] (fermeture logique — le mécanisme de complétion).** Les relations du noyau
ℛ portent des tables de composition (ordres : transitivité ; Allen, RCC-8 : tables
standard). La KB se complète par **propagation de contraintes** (consistance de chemins,
PC-2) : dérivation des relations implicites, détection des incohérences. « Découvrir de
nouveaux chemins » (Déf 8.5) reçoit son moteur ; le nommage filtre ce qui persiste.
« Complet » s'entend : clos sous composition (calculable) — jamais au sens logique
(A-G16). [F7] Chantier : tables de composition pour l'entre-deux/médiane de l'algèbre
médiane produit — à construire ou à trouver dans la littérature.

**[Déf 9.3] (la diagonale — auto-exploration réflexive).** Le système comme son propre
récepteur : Expl(M, M), le protocole W appliqué réflexivement au graphe. Valeur mesurée,
pas décrétée (A-G19) : rendement de la fermeture (faits dérivés / posés, conflits
détectés). Vocabulaire : « réflexif ».

**[Déf 9.4] (concept dynamique et section ergodique).** Un objet suivi dans le temps est
une trajectoire t ↦ x(t) ∈ X ; le **concept dynamique** est son pattern (invariant de
trajectoire : récurrence, cycle, attracteur) ; les formes statiques des §1-§8 sont ses
**sections** (moyennes/médianes temporelles — normes statiques au sens de Reda).
Discipline A-G17 : toute affirmation dynamique se projette sur une section statique
mesurable tant que la récurrence n'est pas établie (test : états récurrents de μ,
session 8). [C 9.4b] Conjecture dérivée : les mots stables nomment les patterns
récurrents, pas les positions instantanées — « c'est dans le mouvement que la langue
prend son sens », version falsifiable.

---

## 10. La carte de complexité du noyau (ajout session 11) + harmonisations v0.2

**[P 10.1] (le pont complexité — via T2).** En d = 1, les relations invariantes sont
les relations FO-définissables dans (ℚ,<) (T2, preuves v0.2) — c'est le domaine des CSP
temporels, dont la complexité est ENTIÈREMENT classifiée : dichotomie P / NP-complet
(Bodirsky & Kára, STOC 2008 / JACM 2010). Carte connue : ordres purs = P (van Beek) ;
Allen = NP-complet, fragment traitable maximal ORD-Horn (Nebel & Bürckert 1995 ;
classification complète Krokhin-Jeavons-Jonsson 2003) ; RCC-8 = NP-complet, fragments
maximaux (Renz & Nebel 1999) ; **entre-deux = NP-COMPLET (Opatrny 1979)** ; ordre
cyclique = NP-complet (Galil & Megiddo 1977). *(Références à re-vérifier en ligne avant
citation.)*

**Conséquences.** (a) **F7 réorienté** : le calcul médian sera NP-dur en général — sa
contribution devient l'identification des fragments traitables maximaux (le geste
Renz-Nebel). (b) **KB ([Déf 8.6], [Déf 9.2])** : la propagation est polynomiale mais
incomplète sur les fragments NP-complets — choix de design à assumer : ℛ restreint à un
fragment traitable, ou propagation sound-but-incomplete documentée. (c) **Papier v2** :
troisième pilier de cadrage — géométrie (Erlangen), information (débit-distorsion),
complexité (dichotomies CSP). Garde-fous : A-G20 (annoncer la borne, jamais la subir en
review), A-G21 (pire cas ≠ usage — mesurer sur les instances réelles).

**[Q 10.2] (ouvertes).** Dichotomie pour les produits (ℚ,<)^d avec relations par axe ;
position de ≈_κ (equality languages) ; médiane vs entre-deux en dureté.

### Harmonisations v0.2 (issues de la relecture adverse des preuves)

- **[Déf 1.2] corrigée** : Mon(X_i) := AUTOMORPHISMES D'ORDRE de X_i (bijections
  strictement croissantes surjectives) — convention unique, voir preuves v0.2.
- **[P 1.4] → [T 1.4]** au sens précis des deux formes d'énoncé (E1 récepteur
  transformé / E2 même récepteur, V_seuils G-stable comme ensemble) — voir preuves v0.2.
- **[C 2.2] → [T 2.2] sous hypothèses restreintes** : axes ≅ ℝ ou ℚ (ou chaînes
  doublement homogènes) ; la restriction est nécessaire (lacunes définissables → L5).
  Statut : fait classique transposé (rangs/DLO/meaningfulness) — citations frontales.
- **F1, F2 : réglés (v0.2)** ; **F6 : réglé au niveau points** (invariant vs équivariant
  précisé, convention de médiane paire) ; F3 doit intégrer le critère sémantique des
  constantes éliminables (L2 corrigée) dans la grammaire I1.
