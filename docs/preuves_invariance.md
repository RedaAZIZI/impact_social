# Preuves — T1 (invariance du coût) et T2 (caractérisation du fragment invariant)

**Statut** : rédaction complète au niveau « brouillon de papier » — hypothèses explicites,
limites annoncées, à faire relire adversarialement avant tout usage en soumission.
Règle les faits nécessaires **F2** (T1) et **F1/F6** (T2, au niveau des configurations
de points) du noyau géométrique v0.1.

**Notations** : celles du noyau formel v0.1 et du noyau géométrique v0.1.
X = ∏_{i=1..d} X_i ; G = ∏_i Mon(X_i) (bijections strictement croissantes de X_i) ;
pour g = (g_1, …, g_d) ∈ G et x ∈ X, g(x) := (g_1(x_1), …, g_d(x_d)).

---

## Théorème 1 (invariance du coût d'explicabilité — ex-[P 1.4], ex-Prop 1)

**Hypothèses.** D une distribution sur X ; M : X → Y, |Y| < ∞ ; R = (V, C) avec
V = V_seuils := { x ↦ 1[x_i ≥ t] : i ≤ d, t ∈ X_i } (vocabulaire de seuils par axe).
Pour g ∈ G : g·D := loi de g(X) pour X ~ D (pousseé en avant), et M^g := M ∘ g⁻¹.

**Énoncé.** Pour tout k ≥ 0 :
F^{g·D}_{M^g, R}(k) = F^{D}_{M, R}(k),
et donc Expl_{g·D}(M^g, R, ε) = Expl_D(M, R, ε) pour tout ε ≥ 0.

**Preuve.**
(1) *La famille V est G-stable.* Pour t ∈ X_i et g_i strictement croissante bijective :
x_i ≥ t ⟺ g_i(x_i) ≥ g_i(t). Donc le prédicat 1[· ≥ g_i(t)] appliqué à la coordonnée
transformée coïncide avec 1[· ≥ t] appliqué à la coordonnée d'origine. (L'équivalence
avec ≥ est exacte : g_i strictement croissante préserve aussi les égalités.)

(2) *Transport des graphes.* Soit H un graphe d'explication sur V (DAG fini, nœuds
étiquetés 1[x_i ≥ t]). Définissons Φ_g(H) := même DAG, chaque étiquette 1[x_i ≥ t]
remplacée par 1[x_i ≥ g_i(t)]. Par (1), pour tout x ∈ X, le chemin suivi par g(x) dans
Φ_g(H) est identique au chemin suivi par x dans H, donc :
g_{Φ_g(H)}(g(x)) = g_H(x) pour tout x ∈ X.   (★)

(3) *Conservation de la fidélité et de la taille.* |Φ_g(H)| = |H| (mêmes nœuds). Et :
fid_{g·D}(Φ_g(H), M^g)
= P_{X~D}[ g_{Φ_g(H)}(g(X)) = M^g(g(X)) ]
= P_{X~D}[ g_H(X) = M(X) ]        (par (★) et M^g∘g = M)
= fid_D(H, M).

(4) *Bijection.* Φ_g est une bijection de l'ensemble des graphes sur V dans lui-même,
d'inverse Φ_{g⁻¹}. Les deux problèmes d'optimisation (taille ↦ meilleure fidélité) sont
donc isomorphes terme à terme : les courbes F(k) coïncident, donc les Expl aussi. ∎

**Remarques.**
- (a) La preuve n'utilise de V que sa G-stabilité : le théorème vaut pour toute famille
  de prédicats close sous l'action de G (prédicats d'intervalle par axe, boîtes,
  prédicats ordinaux par axe). Il ÉCHOUE précisément pour les familles non G-stables —
  ex. les demi-espaces obliques 1[⟨u, x⟩ ≥ t] mélangeant les axes : c'est le cas du
  mélange (Exp 1), qui porte tout le coût, comme prévu par [C 1.5].
- (b) Version discrétisée V_δ (grille de seuils) : l'énoncé vaut en remplaçant la grille
  par son image g(grille) ; si l'on FIXE la grille des deux côtés, l'invariance n'est
  qu'approchée (à un pas de grille près) — c'est exactement le résidu ~10⁻⁴ observé
  parfois dans l'Exp 1b.
- (c) Lien empirique : Exp 1b (linéaire vs tanh par axe : AUC 0.7432/0.7433/0.7433) et
  la repasse « invariance monotone » sur tous les bancs (11/11) sont des instances de T1.

---

## Théorème 2 (caractérisation du fragment invariant — ex-[C 2.2])

**Hypothèses.** Chaque X_i est une chaîne DENSE et SANS EXTRÉMITÉS (ex. ℝ, ℚ, un
intervalle ouvert). φ : X^n → {0,1} un prédicat n-aire (configurations finies de
points), invariant : φ(g(x^1), …, g(x^n)) = φ(x^1, …, x^n) pour tout g ∈ G.

**Définition (type d'ordre d'une configuration).** Pour (x^1, …, x^n) ∈ X^n, son type
d'ordre est le d-uplet des préordres totaux induits sur {1, …, n} par les valeurs par
axe : pour chaque axe i, la donnée, pour chaque paire (a, b), de laquelle des trois
relations x^a_i < x^b_i, x^a_i = x^b_i, x^a_i > x^b_i est vraie.

**Lemme 1 (homogénéité par axe).** Soient u_1 < … < u_k et v_1 < … < v_k dans une
chaîne dense sans extrémités X_i. Alors il existe h ∈ Mon(X_i) avec h(u_j) = v_j pour
tout j.
*Preuve.* Pour X_i = ℝ : interpolation affine par morceaux sur [u_j, u_{j+1}] → [v_j,
v_{j+1}], prolongée affinement au-delà de u_1 et u_k — strictement croissante, bijective.
Pour une chaîne dense sans extrémités générale : argument de va-et-vient de Cantor sur
chaque intervalle (les intervalles ouverts non vides d'une chaîne dense sont denses sans
extrémités ; pour les chaînes dénombrables l'isomorphisme est le théorème de Cantor ;
pour ℝ l'interpolation ci-dessus suffit — on énonce le lemme pour X_i = ℝ ou ℚ, ce qui
couvre tous les usages du cadre). ∎

**Lemme 2 (homogénéité de l'action de G sur les types d'ordre).** Si (x^1, …, x^n) et
(y^1, …, y^n) ont le même type d'ordre, il existe g ∈ G avec g(x^a) = y^a pour tout a.
*Preuve.* Axe par axe : les valeurs distinctes triées (u_1 < … < u_{k_i}) de
(x^1_i, …, x^n_i) et (v_1 < … < v_{k_i}) de (y^1_i, …, y^n_i) ont même longueur k_i et
même affectation des indices (même préordre, donc mêmes classes d'égalité envoyées dans
le même ordre). Le Lemme 1 fournit g_i avec g_i(u_j) = v_j. Poser g = (g_1, …, g_d). ∎

**Énoncé.** Sont équivalents :
(i) φ est G-invariant ;
(ii) φ ne dépend que du type d'ordre de la configuration ;
(iii) φ est une combinaison booléenne FINIE des atomes { x^a_i < x^b_i } et
{ x^a_i = x^b_i } (comparaisons inter-points par axe, sans constante).

**Preuve.**
(iii) ⇒ (i) : chaque atome est invariant (g_i strictement croissante préserve < et =) ;
les combinaisons booléennes d'invariants sont invariantes.
(i) ⇒ (ii) : si deux configurations ont le même type d'ordre, le Lemme 2 les échange par
un g ∈ G, donc φ y prend la même valeur.
(ii) ⇒ (iii) : le nombre de types d'ordre est fini à (n, d) fixés (au plus (nombre de
préordres totaux sur n éléments)^d). Chaque classe de type d'ordre est exactement
définie par la conjonction des atomes qui décrivent son préordre par axe. φ, fonction
des types d'ordre, est la disjonction (finie) des classes qu'il accepte. ∎

**Corollaire 1 (F1 — la grammaire du fragment invariant est bien posée).** Le fragment
invariant de la géométrie ordinale produit est EXACTEMENT le langage des énoncés d'ordre
inter-objets par axe : comparatifs, égalités qualitatives, et tout ce qui s'en compose.
Aucun invariant « exotique » n'existe au niveau des configurations de points. La
grammaire I1 découpe la langue à l'endroit que la mathématique impose.

**Corollaire 2 (F6 — complétude du noyau ℛ, niveau points).** Puisque les ordres par
axe { ≤_i } appartiennent à ℛ et engendrent tous les atomes de (iii), toute relation
n-aire invariante est définissable depuis ℛ. En particulier l'entre-deux et la médiane
sont définissables : B_i(a, x, b) ⟺ (a_i ≤ x_i ≤ b_i) ∨ (b_i ≤ x_i ≤ a_i) ;
med(x¹, …, xⁿ)_i = l'élément médian au sens de l'ordre ≤_i — des énoncés de type
d'ordre. ℛ est complet pour les invariants de configurations de points.

**Limites et extensions (annoncées, non prouvées ici).**
- (L1) *Régions.* Les boîtes étant déterminées par leurs sommets (points), T2 s'étend
  aux prédicats invariants sur les boîtes. Les superpositions (mesures sur boîtes)
  demandent un cadre de plus (invariance en loi) — chantier.
- (L2) *Constantes.* Tout énoncé mentionnant une constante nommée (seuil chiffré, unité)
  sort du fragment par construction — c'est le rôle structurel de W_cal ([P 3.2]) :
  la calibration est l'estimation de ce que l'invariance ne transporte pas.
- (L3) *Chaînes avec extrémités.* Si X_i = [0,1] avec extrémités FIXES (g_i(0)=0,
  g_i(1)=1), de nouveaux invariants apparaissent : « x_i est extrémal ». Remarque
  importante pour l'arité 1 de la session 9 (A-G15) : l'extrémalité n'est un invariant
  QUE si les bornes existent et sont fixées — candidat propre de self-relation.
- (L4) *Densité.* Sans densité (axes discrets), le Lemme 1 exige des cardinalités
  compatibles ; les énoncés de comptage (« il y a exactement 3 valeurs entre a et b »)
  deviennent invariants. À traiter si des axes discrets entrent dans le cadre.

**Positionnement (devoir de littérature — voir REVUE_LITTERATURE.md).** T2 est de la
famille des résultats de « meaningfulness » de la théorie de la mesure (un énoncé sur
une échelle ordinale est significatif ssi invariant par transformations monotones —
Stevens ; Suppes & Zinnes ; Krantz-Luce-Suppes-Tversky ; Roberts) et de l'homogénéité
des chaînes denses (Cantor). La forme produit multi-axes, le lien au coût
d'explicabilité (T1), et l'usage linguistique/architectural (conjecture des invariants,
noyau ℛ, KB) constituent l'apport ; la parenté doit être citée frontalement.

---

## Conséquences sur le noyau géométrique v0.1

- [P 1.4] → **[T 1.4]** (T1 ci-dessus) : **F2 réglé**.
- [C 2.2] → **[T 2.2]** au niveau des configurations de points (T2) : **F1 réglé**
  (modulo relecture adverse), avec les limites L1-L4 comme chantiers dérivés.
- [F6] **réglé au niveau points** (Corollaire 2) ; niveau régions/superpositions :
  chantier L1.
- La grammaire I1 reçoit sa base : le fragment invariant = les énoncés de type d'ordre ;
  les sorties du fragment = les constantes nommées (L2), domaine de W_cal.
