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
