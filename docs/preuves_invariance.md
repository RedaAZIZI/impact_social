# Preuves — T1 (invariance du coût), T2 (le fragment invariant), T3 (la copule) — v0.3

**Statut** : v0.3 = fusion de deux relectures adverses INDÉPENDANTES et complémentaires :
(a) la nôtre (workflow du 2026-07-06, 3 sceptiques — a corrigé T1 : contre-exemple
atomique des grilles, non-surjectivité de tanh, syntaxe des graphes, cadre mesurable) ;
(b) l'étude complémentaire reçue le 2026-07-06 (a corrigé T2 plus profondément : chaîne
rigide de Dushnik-Miller, hypothèse optimale de double homogénéité, Prop 2.5 ; a ajouté
T3-copule, la grammaire I1 à quatre classes, la scission F5a/F5b et le régime
évaluation/satisfiabilité de F7). Le journal de réconciliation est en fin de document.
T1 et T2 restent, pour l'essentiel, des faits classiques transposés ; la valeur est dans
le transfert et l'usage.

**Convention unique (harmonise preuves ↔ noyau géométrique).**
Mon(X_i) := **automorphismes d'ordre** de X_i (bijections strictement croissantes de X_i
SUR X_i). Pour la topologie de l'ordre, cela coïncide avec les homéomorphismes croissants ;
on n'utilise aucune autre topologie. La surjectivité est essentielle (arctan ∉ Mon(ℝ)).
G := ∏_i Mon(X_i), agissant coordonnée par coordonnée.

**Cadre mesurable.** X est muni de la tribu engendrée par les demi-espaces {x : x_i ≥ t}.
Tout g ∈ G est bimesurable : g⁻¹({x_i ≥ t}) = {x_i ≥ g_i⁻¹(t)} (surjectivité de g_i).
M est supposé mesurable ; tout graphe fini sur des prédicats de seuil est mesurable.

**Convention syntaxique.** Un graphe d'explication est un objet SYNTAXIQUE : DAG fini à
nœuds étiquetés par des paires (i, t) ∈ {1..d} × X_i (lues « x_i ≥ t »). fid et |·| ne
dépendent que de la sémantique ; les transformations ci-dessous agissent sur la syntaxe.

---

## Théorème 1 (invariance du coût d'explicabilité — ex-Prop 1, fait F2)

**Énoncé (forme générale, isomorphismes entre chaînes éventuellement distinctes).**
Soient X = ∏ X_i et X′ = ∏ X′_i des produits de chaînes, g_i : X_i → X′_i des
isomorphismes d'ordre, g = (g_1, …, g_d). Soient D une distribution sur X, M : X → Y
mesurable, et V_seuils(X), V_seuils(X′) les vocabulaires de seuils respectifs. Alors,
pour tout k ≥ 0 :
F^{g·D}_{M∘g⁻¹, V_seuils(X′)}(k) = F^{D}_{M, V_seuils(X)}(k),
donc Expl est égal des deux côtés pour tout ε. Le cas X′ = X, g ∈ G est l'énoncé
d'invariance de groupe ; la forme générale couvre aussi les déformations non surjectives
DE ℝ DANS ℝ à la tanh, lues comme isomorphismes ℝ → (−1, 1).

**Preuve.** (1) x_i ≥ t ⟺ g_i(x_i) ≥ g_i(t) (isomorphisme d'ordre). (2) Φ_g : graphe
syntaxique H sur X ↦ même DAG avec étiquettes (i, t) ↦ (i, g_i(t)) — bien défini au
niveau syntaxique, |Φ_g(H)| = |H|, et g_{Φ_g(H)}(g(x)) = g_H(x) pour tout x (le chemin
suivi est identique nœud à nœud, par (1)). (3) fid_{g·D}(Φ_g(H), M∘g⁻¹)
= P_{X~D}[g_{Φ_g(H)}(g(X)) = M(X)] = P_{X~D}[g_H(X) = M(X)] = fid_D(H, M).
(4) Φ_g est une bijection entre graphes syntaxiques sur X et sur X′ (inverse Φ_{g⁻¹},
qui exige la surjectivité de chaque g_i sur X′_i). Les problèmes d'optimisation sont
isomorphes terme à terme. ∎

**Deux formes d'énoncé, à ne pas confondre** (relevé par la relecture adverse) :
- (E1) *récepteur transformé* : Expl_D(M, R, ε) = Expl_{g·D}(M∘g⁻¹, R∘g⁻¹, ε) — vraie
  pour TOUTE famille V (tautologique au niveau syntaxique) ; c'est la forme [P 1.4] du
  noyau géométrique.
- (E2) *même récepteur des deux côtés* : vraie ssi la famille est stable comme ENSEMBLE
  sous g (V_seuils complet l'est ; une grille finie V_δ ne l'est pas). T1 ci-dessus est
  (E2) pour V_seuils. Le passage « [P 1.4] → [T 1.4] » s'entend en ce sens précis.

**Lemme 1.q (grilles fixes — version quantitative honnête ; remplace la remarque (b)
v0.1, RÉFUTÉE).** Pour une grille fixe V_δ des deux côtés, l'invariance peut échouer
GRAVEMENT si D a des atomes : contre-exemple (sceptique T1) — d = 1,
D = ½δ_{0.04} + ½δ_{0.06}, M = 1[x ≥ 0.05], grille de pas 0.1 : F = ½ pour tout budget
côté source, F(1) = 1 côté image par un g bien choisi — écart ½, quel que soit δ.
Sous hypothèse de régularité — masse de bande contrôlée, sup_t P[x_i ∈ [t, t+δ)] ≤ m(δ)
par axe — on a en revanche |F^{g·D}_{M∘g⁻¹,V_δ}(k) − F^{D}_{M,V_δ}(k)| ≤ C·k·m(δ)
(chaque seuil se déplace d'au plus une maille et ne déplace que la masse d'une bande).
*À faire : vérifier que les données de l'Exp 1b satisfont l'hypothèse (elles sont
continues U[0,1] : oui) — le résidu ~10⁻⁴ observé est alors couvert.*

**Remarque (familles non stables).** La G-stabilité est SUFFISANTE, pas nécessaire
(contre-exemple : V_ℚ sur ℝ avec D sans atomes — invariance exacte par densité). Pour
les demi-espaces obliques, il EXISTE des (D, M, g, k) rompant l'égalité — c'est l'Exp 1.
La caractérisation exacte des familles invariantes est OUVERTE.

**Positionnement (honnêteté imposée par la relecture).** L'invariance des arbres à
seuils sous transformations monotones par axe est un fait folklore depuis CART
(Breiman, Friedman, Olshen & Stone 1984 ; rappelé dans Hastie-Tibshirani-Friedman,
*ESL*), caveat de discrétisation compris (cf. arXiv:1611.04561). **La nouveauté exacte,
à dire frontalement en soumission** (formulation de l'étude complémentaire, adoptée) :
l'apport de T1 n'est pas « un arbre à seuils est invariant » mais que **toute la courbe
F(k) — le front taille↦fidélité pour expliquer un M ARBITRAIRE à un récepteur à
seuils — est un invariant de la géométrie ordinale** : le coût d'explicabilité lui-même,
pour tout budget, tout ε, tout M (y compris hors de la classe des arbres).

---

## Théorème 2 (le fragment invariant — fait F1, version corrigée)

**Hypothèse (H) — la double homogénéité (adoptée de l'étude complémentaire ; remplace
et généralise notre restriction v0.2 à ℝ/ℚ).** Une chaîne (X_i, ≤) est **doublement
homogène** si pour tous a < b et c < d dans X_i, il existe h ∈ Aut(X_i, ≤) avec
h(a) = c et h(b) = d. Exemples : ℝ, ℚ, tout intervalle ouvert réel, ℝ∖ℚ.
Contre-exemples : chaînes finies ≥ 3 points, ℤ, les chaînes rigides. **(H)** : chaque
X_i est un singleton ou une chaîne doublement homogène d'au moins 3 points. Sous (H),
X_i (≥ 3 points) est automatiquement dense, sans extrémités, et Aut(X_i) transitif.

**Pourquoi « dense sans extrémités » ne suffit pas (deux familles de contre-exemples,
issues des deux relectures — complémentaires).**
(a) *Les lacunes* (notre relecture) : X₁ = (0,1) ∪ (1,2), ou ℝ∖{0} — la lacune de
Dedekind est unique donc fixée par tout automorphisme ; φ(x) := 1[x < 1] est invariant,
non constant, hors type d'ordre. → limite L5.
(b) *La rigidité* (étude complémentaire — le coup fatal) : **Dushnik & Miller (1940)**
construisent X ⊂ ℝ dense DANS ℝ, de cardinal 2^ℵ⁰, dont le seul automorphisme est
l'identité. Dense en soi, sans extrémités, sans lacune exploitable — et pourtant TOUT
prédicat y est invariant. La densité même dans ℝ ne suffit pas : il faut l'homogénéité.

**Lemme 2.2 (2 ⇒ n, à support contrôlé — étude complémentaire, preuve autonome).** Si
X_i est doublement homogène (≥ 3 points), alors pour tous a < b dans X_i ∪ {±∞}, tout
n et toutes suites u₁ < … < u_n, v₁ < … < v_n dans (a, b), il existe h ∈ Aut(X_i) avec
h(u_j) = v_j et h = id hors de (a, b). *Preuve : cas n = 1 par recollement de deux
automorphismes ((a,u)↦(a,v) et (u,b)↦(v,b)) ; récurrence en poussant u₁ sur v₁ puis en
travaillant dans (v₁, b) — le contrôle du support rend la récurrence licite. C'est un
cas du fait classique « doublement homogène ⇒ n-homogène » (Glass, *Ordered Permutation
Groups*) ; la preuve par recollement rend le document autonome.* ∎

**Lemme 2.3 (homogénéité de G sur les types d'ordre).** Sous (H) : axe par axe via le
Lemme 2.2 avec (a, b) = (−∞, +∞) (les classes d'égalité, de même motif, se
correspondent). ∎

**Énoncé (Théorème 2.4).** Sous (H), pour φ : X^n → {0,1} :
φ est G-invariant ⟺ φ ne dépend que du type d'ordre ⟺ φ est combinaison booléenne
finie des atomes {x^a_i < x^b_i} et {x^a_i = x^b_i}. *Preuve : (iii)⇒(i) atomes
invariants ; (i)⇒(ii) Lemme 2.3 ; (ii)⇒(iii) finitude des types d'ordre à (n, d)
fixés.* ∎

**Prop 2.5 (optimalité de (H) — étude complémentaire).** Si l'équivalence (i)⟺(ii)
vaut pour toute arité, alors chaque X_i est un singleton ou une chaîne doublement
homogène ≥ 3 points. *Preuve : |X_i| = 2 → φ = 1[x_i = max] casse l'arité 1 ; X_i non
doublement homogène → deux orbites de paires croissantes existent, et l'indicatrice
d'orbite casse l'arité 2.* ∎ **(H) n'est pas une commodité de preuve : c'est la
frontière exacte du théorème.**

**Corollaire 1 (F1).** La grammaire du fragment invariant est bien posée : sous (H),
les invariants sont exactement les énoncés d'ordre inter-objets par axe — et par la
Prop 2.5, (H) est exactement le domaine de validité de cette grammaire.

**Corollaire 2 (F6, niveau points — reformulé).** Les ordres {≤_i} ⊆ ℛ engendrent tous
les atomes, donc toute RELATION n-aire invariante est définissable depuis ℛ. Précisions
imposées par la relecture : (a) la médiane est une FONCTION, donc ÉQUIVARIANTE
(med∘g = g∘med), pas invariante — c'est son GRAPHE, le prédicat (n+1)-aire
1[y = med(x¹, …, xⁿ)], qui est invariant et définissable ; (b) pour n pair, fixer la
convention (médiane basse) ; la médiane ternaire de l'algèbre médiane ([P 8.3] du noyau)
est sans ambiguïté ; (c) la meaningfulness de la médiane sur échelle ordinale est
archi-classique (Stevens ; Roberts 1979) — pointer, ne pas redémontrer.

**Limites (corrigées et complétées).**
- (L1) *Régions* : inchangée (boîtes via leurs sommets ; superpositions = chantier).
- (L2) *Constantes — reformulée* : un énoncé sort du fragment ssi sa valeur de vérité
  DÉPEND effectivement de la constante (critère sémantique) — « x ≥ 12 000 ∨ x < 12 000 »
  mentionne une constante et reste invariant. Conséquence pour I1/F3 : le classifieur
  d'annotation sera syntaxique avec cas frontière systématiques (tautologies, constantes
  éliminables) — critère opérationnel à déclarer AVANT l'annotation.
- (L3) *Extrémités* : la fixation des bornes par les automorphismes est AUTOMATIQUE
  (pas une stipulation) ; « x est extrémal » devient invariant dès |X_i| ≥ 2.
- (L4) *Axes discrets* : la relation de couverture (successeur) est invariante dans
  toute chaîne non dense ; les comptages exacts aussi sur ℤ. Corpus existant : Bodirsky,
  Martin & Mottet, JACM 2018 (CSP temporels discrets) — citer si L4 est développée.
- (L5) *Homogénéité (précisée par la fusion v0.3)* : hors (H), deux pathologies
  distinctes cassent le théorème — les LACUNES définissables (nos contre-exemples
  (0,1)∪(1,2), ℝ∖{0}) et la RIGIDITÉ (Dushnik-Miller : dense dans ℝ, Aut = {id}).
  La Prop 2.5 clôt la question : (H) est la frontière exacte, L5 n'est plus une liste
  ouverte de pathologies mais un théorème de caractérisation.

**Positionnement (requalifié — verdict du sceptique littérature, confirmé par le front
mesure).** T2 est un fait classique sous trois habillages, à citer frontalement :
(i) *statistique* — les rangs sont l'invariant maximal du groupe des transformations
strictement croissantes (Lehmann & Romano ; Hájek & Šidák) ; en produit, les rangs par
composante (Puri & Sen 1971) ; (ii) *théorie des modèles* — préservé par toutes les
bijections croissantes ⟺ FO-définissable dans (ℚ,<) (Ryll-Nardzewski + élimination des
quantificateurs de DLO ; énoncé tel quel chez Bodirsky & Kára, STOC 2008) ;
(iii) *théorie de la mesure* — meaningfulness ordinale (Suppes & Zinnes 1963 ; KLST
vol. III 1990 ; Roberts 1979 ; Narens 2002) ; côté FONCTIONS, la caractérisation
complète existe (Marichal, Mesiar & Rückschlossová 2005 ; survol Marichal & Mesiar
2009). Nuance relevée par le front 1 : la version ÉNONCÉS sur produit d'échelles
ordinales indépendantes ne semble pas publiée telle quelle — mais elle se DÉRIVE du
cadre existant ; la revendication honnête est « théorème de transfert, instancié pour
notre usage », pas « théorème nouveau ». **La nouveauté du programme est ailleurs** :
le lien au coût d'explicabilité (T1+Expl), la conjecture linguistique (I2/I3), le calcul
médian (F7, chantier vierge — front 3), et le pont superposition↔coût récepteur (G3,
ouvert — front 5).

---

---

## Théorème 3 (l'invariant maximal en loi est la copule — étude complémentaire, adopté ;
ferme L1 au niveau des lois)

**[T 3.1].** X = ℝᵈ, G = ∏ Mon(ℝ), 𝒟 = lois à marginales de f.r. continues strictement
croissantes sur ℝ. Alors (a) la copule de g·D est celle de D pour tout g ∈ G
(Sklar ; invariance classique : Schweizer & Wolff 1981 ; Nelsen 2006 §2.4) ;
(b) D, D′ ∈ 𝒟 sont dans la même G-orbite SSI C_D = C_{D′} (poser g_i := (F′_i)⁻¹∘F_i ;
unicité de Sklar). ∎

**[Cor 3.2].** Les fonctionnelles G-invariantes des lois de 𝒟 = les fonctionnelles de
la copule (τ de Kendall, ρ de Spearman, dépendance de queue…) ; **l'indépendance est un
énoncé du fragment invariant** (copule produit). Slogan exact : *la statistique
non-paramétrique est la statistique du fragment invariant* — T2 en est la version
échantillon (les rangs), T3 la version en loi.

**Remarque (profil de support — écho de L3).** Sur supports intervalles S_i ⊊ ℝ,
l'invariant maximal devient (copule ; profil des extrémités du support) — ex. Exp(1)
et N(0,1) : même copule en d=1, orbites distinctes. Deux conventions possibles (axes
abstraits X_i := S_i, ou axes plongés dans ℝ) : **le noyau doit déclarer laquelle il
adopte, axe par axe.** [Décision à prendre — portée dans le noyau §11.]

**Limite L1′ (marginales à atomes).** Copule unique seulement sur Ran F ; extensions
« checkerboard » (Genest & Nešlehová 2007). Rejoint L4. Chantier petit et balisé.

---

## F5 scindé (correction épistémique adoptée de l'étude complémentaire)

- **F5a (l'ex-F5, requalifié TEST UNITAIRE).** L'issue du design synthétique
  (repondération par axe) est GARANTIE par T1 : **poids évidentiel nul** sur le monde.
  Utile pour vérifier le pipeline, rien de plus. Notre issue X-45 était mal calibrée —
  corrigée.
- **F5b (l'expérience réelle).** Récepteurs HUMAINS : le coût de compréhension (erreurs,
  temps, questions de calibration) est-il invariant sous re-calibration monotone des
  stimuli, et croît-il sous mélange hors-G ([C 1.5]) ? C'est une expérience
  psycholinguistique — elle teste la CONJECTURE, pas le théorème, et c'est elle qui
  porte le poids évidentiel. À protocoler avant tout investissement.

---

## Journal de réconciliation v0.3 (qui a trouvé quoi, qu'est-ce qui a été retenu)

| Point | Notre relecture (v0.2) | Étude complémentaire | Retenu en v0.3 |
|---|---|---|---|
| T1 : grilles fixes | Contre-exemple atomique (écart ½) + lemme quantitatif en m(δ) | Affirme « exacte à un pas de grille près » — **réfuté par notre contre-exemple** | **Notre version** (leur remarque (b) est fausse pour D atomique) |
| T1 : tanh / surjectivité | Forme générale par isomorphismes entre chaînes distinctes | Garde g ∈ Aut(X_i) et cite l'Exp 1b directement — la non-surjectivité de tanh n'est pas traitée | **Notre version** (la leur ne couvre pas tanh littéralement) |
| T1 : positionnement | Folklore CART, transposition | Nomme la nouveauté exacte (toute la courbe F(k), M arbitraire) | **Leur formulation**, meilleure |
| T2 : hypothèse | Restriction à ℝ/ℚ (suffisante mais pas optimale) | (H) double homogénéité + Dushnik-Miller + **Prop 2.5 (optimalité)** | **Leur version** (strictement plus forte) |
| T2 : Corollaire 2 | Précisions invariant/équivariant, convention médiane paire | Non traité | **Nos précisions conservées** |
| T3 (copule) | Absent | Théorème complet + profil de support + L1′ | **Adopté** |
| Grammaire I1 | Critère sémantique L2 (constantes éliminables) | 4 classes I/C/A/N + bifurcation des numéraux + Kennedy/Klein | **Fusion** : leurs 4 classes + notre critère L2 (voir I1_grammaire) |
| F5 | Expérience prévue telle quelle (X-45) | Scission F5a (poids nul)/F5b (humains) | **Leur correction** — la nôtre était mal calibrée |
| F7 / complexité | Session 11 : carte NP, fragments traitables | Régime évaluation vs satisfiabilité + garde-fou | **Fusion** ; leur « A-G20 » renuméroté **A-G22** (collision avec notre A-G20 existant) |

## Conséquences sur le noyau géométrique (mises à jour v0.3)

- **F2 réglé** : T1 (forme isomorphismes, E1/E2, lemme quantitatif des grilles).
- **F1 réglé sous (H)**, avec optimalité (Prop 2.5) : la restriction n'est plus un
  choix, c'est la frontière exacte. Fait classique transposé — citations frontales.
- **F6 réglé au niveau points** ; **L1 fermé au niveau des lois** par T3 (reste L1′).
- **F5 → F5a/F5b** (X-45 à requalifier). **F7** : régime évaluation (polynomial, la KB
  vit là) vs satisfiabilité (NP dès l'entre-deux) — garde-fou A-G22 : aucune boucle de
  fermeture sur un fragment dont la satisfiabilité n'est pas prouvée polynomiale.
- **[Déf 1.2] du noyau** : Mon(X_i) = automorphismes d'ordre (convention unique).
- **I1/F3** : grammaire à quatre classes (voir `docs/I1_grammaire_fragment_invariant.md`)
  intégrant le critère sémantique L2 ; pilote corpus exécuté (voir
  `docs/RESULTATS_PILOTE_F3.md` — statut pilote, ne remplace pas F3).
