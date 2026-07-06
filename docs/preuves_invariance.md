# Preuves — T1 (invariance du coût) et T2 (le fragment invariant) — v0.2

**Statut** : v0.2, corrigée après relecture adverse (workflow du 2026-07-06, 3 sceptiques,
verdicts « major » intégrés). Les énoncés v0.1 étaient réparables mais fautifs sur la
généralité (T2) et sur trois remarques (T1) ; cette version intègre les contre-exemples
trouvés et REQUALIFIE la nouveauté (voir Positionnement — T1 et T2 sont, pour l'essentiel,
des faits classiques transposés ; la valeur est dans le transfert et l'usage).

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
(Breiman, Friedman, Olshen & Stone 1984), caveat de discrétisation compris
(cf. Bland et al., arXiv:1611.04561). T1 est la transposition de ce folklore au
fonctionnel Expl_D (courbes fidélité/budget) — la formulation est nouvelle, pas le
mécanisme. Citer frontalement.

---

## Théorème 2 (le fragment invariant — fait F1, version corrigée)

**Hypothèses (RESTREINTES — la v0.1 était réfutée).** Chaque X_i est une chaîne
isomorphe comme ordre à ℝ ou à ℚ (ce qui couvre les intervalles ouverts de ℝ ou ℚ —
les seuls usages du cadre). Bon niveau de généralité si besoin : chaînes **doublement
homogènes** (Mon(X_i) transitif sur les paires croissantes ; cf. Glass, *Ordered
Permutation Groups*).

**Pourquoi la restriction est nécessaire (contre-exemples de la relecture adverse).**
« Dense sans extrémités » ne suffit PAS : (a) X₁ = (0,1) ∪ (1,2) est dense sans
extrémités, mais sa lacune de Dedekind en 1 est unique donc fixée par tout
automorphisme — φ(x) := 1[x < 1] est G-invariant, non constant, et n'est PAS un énoncé
de type d'ordre (toutes les configurations à 1 point ont le même type). (b) Idem
ℝ∖{0}. Les LACUNES définissables engendrent des invariants exotiques → limite L5.

**Lemme 1 (homogénéité, restreint).** Dans X_i ≅ ℝ : interpolation affine par morceaux
(prolongée affinement) envoie u_1 < … < u_k sur v_1 < … < v_k. Dans X_i ≅ ℚ :
va-et-vient de Cantor par intervalles (la dénombrabilité est requise — l'argument
« va-et-vient général » de la v0.1 était invalide). ∎

**Lemme 2 (homogénéité de G sur les types d'ordre).** Comme en v0.1, axe par axe via le
Lemme 1 (les classes d'égalité, de même motif des deux côtés, se correspondent). ∎

**Énoncé.** Sous les hypothèses restreintes, pour φ : X^n → {0,1} :
φ est G-invariant ⟺ φ ne dépend que du type d'ordre ⟺ φ est combinaison booléenne
finie des atomes {x^a_i < x^b_i} et {x^a_i = x^b_i}. *Preuve inchangée (orbites =
types d'ordre ; finitude des types à (n, d) fixés).* ∎

**Corollaire 1 (F1).** La grammaire du fragment invariant est bien posée : sur des axes
≅ ℝ/ℚ, les invariants sont exactement les énoncés d'ordre inter-objets par axe.

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
- (L5) *Lacunes/homogénéité (NOUVELLE)* : les chaînes denses sans extrémités NON
  homogènes ont des coupures définissables (lacunes, cofinalités) qui engendrent des
  invariants hors type d'ordre — d'où la restriction d'hypothèses ci-dessus.

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

## Conséquences sur le noyau géométrique v0.1 (mises à jour v0.2)

- **F2 réglé** : T1 prouvé (forme isomorphismes entre chaînes, deux formes d'énoncé
  distinguées, lemme quantitatif pour les grilles) — relu adversarialement, corrections
  intégrées.
- **F1 réglé sous hypothèses restreintes** (axes ≅ ℝ/ℚ, ou doublement homogènes) ; la
  restriction est NÉCESSAIRE (contre-exemples L5). Statut : fait classique transposé,
  citations frontales obligatoires dans le papier.
- **F6 réglé au niveau points**, avec les précisions invariant/équivariant et la
  convention de médiane paire ; niveau régions/superpositions : chantier L1.
- **[Déf 1.2] du noyau** à harmoniser : Mon(X_i) = automorphismes d'ordre (cette
  convention fait foi).
- I1/F3 : intégrer le critère sémantique de L2 (constantes éliminables) dans la
  grammaire AVANT toute annotation.
