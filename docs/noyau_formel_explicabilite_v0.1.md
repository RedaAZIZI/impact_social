# Explicabilité relationnelle — noyau formel v0.1

**Périmètre** : claims 1 (loi θ) et 2 (unification). La persuasion (Δ) est hors périmètre. La résonance n'apparaît que là où elle tombe gratuitement des définitions.

**Statut des énoncés** : [T] théorème avec preuve esquissée ici · [P] proposition (preuve courte) · [Cor] corollaire · [C] conjecture / chantier · [Déf] définition.

---

## 0. Les trois claims du papier

**C1 (unification).** Il existe une quantité unique Expl_D(M, R, ε), paramétrée par le vocabulaire du récepteur, dont les méthodes XAI existantes — distillation en arbre, LIME/Anchors, contrefactuels, CBM/TCAV, simulatabilité, XAI dialogique — sont des cas particuliers, des instruments d'estimation, ou des protocoles auxquels manque la métrique. (Théorème d'identification en θ = 0 + table de plongements, §3.)

**C2 (loi θ).** Dans un modèle minimal exactement soluble, le coût d'explication suit une loi exacte **Expl = Θ(sin(2θ)/ε)** : continue, monotone sur (0, π/4], maximale à 45°, égale à 1 en θ = 0. Les expériences synthétiques testent la persistance de la loi au-delà du modèle minimal. (§4.)

**C3 (statique ⇒ interactif) — le résultat qui soude le papier.** Le coût interactif (nombre de questions W) est contraint par la loi statique : après T questions de taille ≤ s, la fidélité atteignable est majorée par F(sT) ≤ 1 − c·sin(2θ)/(sT). Le plafond de l'Exp 2 (71 %, non-convergence) se **dérive** de la loi de l'Exp 1 : les deux expériences mesurent la même quantité par deux instruments. (§5.)

**Positionnement en une phrase** : le tournant pragmatique de la XAI (van Fraassen 1980 ; Miller 2019 ; Páez 2019) affirme que l'explication est relative à l'audience ; nous rendons cette relativité *mesurable* et identifions le désalignement de base comme variable causale, continue et quantifiée du coût d'explication.

---

## 1. Objets

**[Déf 1.1] (cadre).** X ⊆ ℝ^d, distribution D sur X, modèle M : X → Y avec |Y| < ∞.

**[Déf 1.2] (vocabulaire engendré par un repère).** Pour un repère orthonormé B = (u_1, …, u_d) :
V(B) := { x ↦ 1[⟨u_i, x⟩ ≥ t] : i ≤ d, t ∈ ℝ }.
Pour les arguments de comptage : version discrétisée V_δ(B) (seuils sur grille de pas δ), pool de taille P.
Récepteur général : R = (V_R, C_R), où V_R est un ensemble quelconque de prédicats (pas nécessairement linéaires — cas CBM : détecteurs de concepts) et C_R un budget de capacité.

**[Déf 1.3] (graphe d'explication).** G = DAG fini ; nœuds internes étiquetés par des prédicats de V_R, arêtes par leurs valeurs, feuilles par Y. Fonction calculée g_G : X → Y. Taille |G| = nombre de nœuds internes.

**[Déf 1.4] (fidélité).** fid_D(G, M) := P_{X~D}[ g_G(X) = M(X) ].

**[Déf 1.5] (explicabilité, courbe, AUC).**
Expl_D(M, R, ε) := min{ |G| : G sur V_R, fid_D(G, M) ≥ 1 − ε } (= ∞ si l'ensemble est vide).
Courbe : F_{M,R}(k) := sup{ fid_D(G, M) : |G| ≤ k }, croissante en k.
AUC_K := (1/K) · Σ_{k=1..K} F(k).

**[Déf 1.6] (repère intrinsèque et θ).** Attention : l'angle « aux axes d'entrée » n'est PAS la bonne variable (contre-exemple §4.4). On définit le repère intrinsèque de M :
B*_M ∈ argmin_B Expl_D(M, (V(B), ∞), ε₀),
puis θ(M, R) := angle principal maximal entre B_R et B*_M.
Dans les mondes synthétiques, B*_M est contrôlé par construction — c'est ce qui rend θ causalement manipulable.
[C 1.6a] Existence/mesurabilité de l'argmin sur O(d) (semi-continuité ; technique, à rédiger).
[C 1.6b] Extension de θ aux vocabulaires non linéaires : problème ouvert assumé. Candidat : coût de traduction mutuel (taille minimale espérée d'un graphe exprimant les prédicats d'un vocabulaire dans l'autre) ; se réduit à une fonction de θ dans le cas linéaire.

**[Déf 1.7] (protocole W et coût interactif).** Soit G* un graphe minimal ε₀-fidèle de M sur V_R (référence). Requête w = (x, y') ; réponse W(x, y') = sous-graphe pivot : différence symétrique entre le chemin de x dans G* et le chemin contrefactuel minimal menant à y', prédicats et seuils inclus ; taille de réponse plafonnée à s.
QC_s(M, R, ε) := nombre minimal (sur les stratégies du récepteur) de requêtes après lesquelles le récepteur peut produire Ĝ avec fid(Ĝ, M) ≥ 1 − ε — au pire cas sur la classe de modèles (voir §5 pour la raison du pire cas).

---

## 2. Structure

**[P 2.1] (monotonie au vocabulaire).** V_R ⊆ V_{R'} ⇒ F_{M,R'}(k) ≥ F_{M,R}(k) pour tout k ; donc Expl décroît. *Preuve : immédiate.*
Remarque : c'est ce qui rend la « résonance » bien définie — le gain marginal de fidélité par prédicat ajouté est la dérivée discrète de cette monotonie. Hors périmètre ici.

**[P 2.2] (caractérisation du plateau).**
F_{M,R}(∞) = E_D[ max_y P( M(X) = y | σ(V_R) ) ],
où σ(V_R) est la tribu engendrée par les prédicats.
*Preuve (esquisse).* Tout G fini n'utilise qu'un nombre fini de prédicats et g_G est mesurable pour l'algèbre finie qu'ils engendrent ; réciproquement, l'arbre complet sur m prédicats réalise le meilleur prédicteur mesurable pour cette algèbre. Le sup sur les sous-familles finies converge vers le membre de droite par convergence de martingale le long d'une filtration engendrante (V_R supposé séparable ; vrai en version discrétisée). ∎(esquisse)

**[Cor 2.3] (dichotomie des régimes d'inexplicabilité).**
(a) **Régime informationnel** : V_R pauvre (fini/grossier) ⇒ F(∞) < 1. Le plafond est une erreur de Bayes conditionnelle — incompressible même à budget infini.
(b) **Régime budgétaire** : V_R riche (ex. seuils continus dans un repère quelconque : σ(V(B)) = tribu borélienne, donc F(∞) = 1) mais budget |G| ou nombre de questions borné ⇒ plafond de complexité.

**Diagnostic Exp 2 (à exécuter).** Si le protocole a utilisé un pool fini de prédicats : calculer numériquement E[max_y P(M | σ(pool))] sur le monde synthétique et comparer à 0.71. Égalité ⇒ régime (a). 0.71 strictement en dessous ⇒ régime (b) : c'est le budget de questions qui mordait. L'article doit dire lequel — un reviewer le demandera.

---

## 3. Unification (claim C1)

**[T 3.1] (identification en θ = 0).** Si V_R = V(B*_M) — seuils sur les coordonnées natives de M — alors le programme Expl est exactement la distillation minimale en graphe/arbre axis-aligned, et TREPAN (Craven & Shavlik 1996), les surrogates CART et les soft decision trees (Frosst & Hinton 2017) en sont des heuristiques réalisables.
*Preuve : correspondance de définitions — classes d'hypothèses et objectif coïncident.* ∎
Valeur : conceptuelle (théorème de cadrage). À présenter comme tel, jamais comme un résultat profond.

**[Table 3.2] (plongements — chaque ligne vérifiable indépendamment).**

| Méthode | Lecture dans le cadre | Statut |
|---|---|---|
| Distillation arbre (TREPAN, CART, soft trees) | Expl avec θ = 0, D globale | identité [T 3.1] |
| Anchors (Ribeiro et al. 2018) | graphe à un chemin (règle), D locale | plongement exact |
| LIME | surrogate additif, D = noyau local autour de x, base supposée = base de M | plongement (changement de D et de classe) |
| Contrefactuels (Wachter et al. 2017) | réponse W(x, y') réduite au croisement de frontière minimal | cas particulier de W |
| TCAV (Kim et al. 2018) | alignement entre directions internes de M et V_R : **estimateur local de θ** | instrument de mesure |
| CBM (Koh et al. 2020) | contraindre M à l'image d'un petit G sur V_R : **minimisation d'Expl à la conception** | design-time Expl |
| Simulatabilité (Doshi-Velez & Kim 2017 ; Hase & Bansal 2020) | estimation empirique de fid(G_R, M), G_R = modèle interne du récepteur | métrique cible du protocole |
| XAI dialogique (Madumal et al. 2019 ; arXiv:2408.06960) | protocoles W **sans métrique de coût** | QC est la métrique manquante |

Formulation à employer dans l'article : « ces méthodes ne sont pas concurrentes du cadre ; elles en sont des points, des estimateurs, ou des protocoles ».

---

## 4. La loi θ (claim C2)

**Modèle minimal.** X = [0,1]², D uniforme, M_θ = 1[ x₂ ≥ x₁·tan θ + b ] (frontière passant par le centre), θ ∈ (0, π/4]. Récepteur R₀ : seuils axis-aligned dans le repère standard.

**[T 4.1] (loi de l'escalier, bornes appariées).** Il existe c₁, c₂ > 0 tels que
c₁ · sin(2θ)/ε ≤ Expl(M_θ, R₀, ε) ≤ c₂ · sin(2θ)/ε.

*Preuve (esquisse).*
**Borne inférieure.** Un graphe à k nœuds utilise V coupes verticales et H horizontales, V + H ≤ k. g_G est constante sur chaque cellule de l'arrangement (toutes les valeurs de prédicats y sont constantes — vrai pour un DAG, pas seulement un arbre). Découper en bandes verticales de largeurs a_i (Σ a_i = 1) : dans la bande i, la frontière monte de a_i·tan θ et traverse h_i + 1 cellules (Σ h_i ≤ H) ; l'erreur dans la bande est ≥ c·tan θ · a_i²/(h_i + 1) (aire triangulaire minimale entre le segment et toute approximation constante par cellule — lemme de cellule, ~10 lignes à rédiger). Par Cauchy-Schwarz : Σ a_i²/(h_i+1) ≥ (Σ a_i)²/Σ(h_i+1) ≥ 1/(k+1). D'où erreur ≥ c·tan θ/(k+1) ≥ (c/2)·sin 2θ/(k+1), puisque tan θ ≥ sin 2θ / 2. Inverser en k.
**Borne supérieure.** Escalier uniforme à j = ⌊k/2⌋ marches : erreur = tan θ/(2j) ≤ 2·sin 2θ/k pour θ ≤ π/4 (car cos²θ ≥ 1/2). ∎(esquisse — constantes à soigner)

**[Cor 4.2] (signatures falsifiables).**
(i) Courbe : F(k) = 1 − Θ(sin 2θ / k) ⇒ pente −1 en log-log de (1 − F) contre k.
(ii) **Collapse** : k·(1 − F(k)) tracé contre sin(2θ) doit être affine — toutes les courbes de l'Exp 1 doivent s'effondrer sur une droite. C'est LE graphe du papier.
(iii) Maximum du coût à θ = 45° et symétrie θ ↔ 90° − θ (si le balayage de l'Exp 1 dépasse 45°, test gratuit déjà dans les données).
(iv) Continuité en θ → 0 : Expl → 1, avec sensibilité initiale forte (~ 4θ/ε) : de petits désalignements coûtent déjà.

**[C 4.3] (dimension d).** Frontières linéaires en dimension d, désalignement décrit par les angles principaux (θ_1, …, θ_m) : conjecture Expl = Θ(f(sin 2θ_1, …, sin 2θ_m)/ε), f à déterminer (esquisse par produits de plans 2D à faire). Laisser en extension, pas dans le corps.

**[4.4] (avertissement de non-monotonie — pourquoi Déf 1.6 est nécessaire).** Contre-exemple : si M est un arbre axis-aligned dans un repère B' tourné de 30° par rapport aux coordonnées d'entrée, alors le récepteur « tourné de 30° » est parfaitement aligné et le récepteur « identité » ne l'est pas. La variable causale est l'angle à B*_M (repère intrinsèque), pas aux axes d'entrée. Toute figure de l'article doit être étiquetée θ = angle à B*_M.

---

## 5. Statique ⇒ interactif (claim C3)

**[P 5.1] (borne inférieure de comptage).** Si G* a N nœuds et chaque réponse en révèle ≤ s, alors QC_s ≥ N/s. *Preuve : comptage.* ∎

**[P 5.2] (plafond interactif — version pire-cas, esquisse).** Sur la famille {M_θ,b : b ∈ [0,1]} (offset inconnu du récepteur), après T requêtes de taille ≤ s, toute estimation Ĝ certifiable n'utilise que ≤ sT paires (prédicat, seuil) révélées ; donc, au pire cas,
fid(Ĝ, M) ≤ F(sT) ≤ 1 − c · sin(2θ)/(sT).
*Esquisse : argument d'adversaire — l'environnement reste cohérent avec toutes les réponses données tout en déplaçant la frontière hors des cellules révélées. Le point délicat (empêcher le récepteur de deviner des seuils non révélés) est la raison du pire cas sur b ; la version minimax propre est un chantier.* ∎(esquisse)

**[Cor 5.3] (les deux expériences n'en sont qu'une — argument central du papier).** Le plafond de l'Exp 2 (71 %, non-convergence en base désalignée) est la trace interactive de la loi statique de l'Exp 1 : plafond ≈ F(s·T_max). Prédiction quantitative : le niveau du plafond doit varier comme 1 − c·sin(2θ)/(s·T_max) quand on fait varier θ ET le budget de questions T_max — deux boutons expérimentaux, une seule loi. Statique et interactif sont deux instruments de mesure de la même quantité.

**[P 5.4] (borne supérieure alignée, par réduction).** Si M est exactement un graphe de taille N sur V_R (θ = 0), l'apprentissage exact par requêtes (Angluin 1988 ; Bshouty 1995, monotone theory, pour les arbres de décision) donne une reconstruction en poly(N) requêtes d'appartenance + équivalence ; une requête W est plus informative qu'une requête d'appartenance (elle livre le chemin), donc QC ≤ poly(N). Constantes et adaptation au W exact : à rédiger. Cohérent avec l'Exp 2 alignée (~6 questions, 97.9 %).

---

## 6. Programme expérimental immédiat (sur données existantes)

**E1 — Collapse sin 2θ.** Re-tracer les courbes de l'Exp 1 en k·(1 − F(k)) contre sin(2θ). Coût : une après-midi sur le code existant. Si ça marche : figure centrale du papier. Si ça échoue : la loi minimale ne persiste pas telle quelle hors du modèle 2D — documenter la structure de la déviation (c'est aussi un résultat, à condition qu'elle soit interprétable).
**E2 — Symétrie 45°.** Si le balayage de l'Exp 1 dépasse 45° : vérifier θ ↔ 90° − θ.
**E3 — Régime du plateau [Cor 2.3].** Calculer le F(∞) informationnel du pool de prédicats de l'Exp 2 ; trancher régime (a) vs (b). Une journée.
**E4 — Loi du plafond interactif [Cor 5.3].** Re-faire l'Exp 2 en variant T_max à θ fixe ; vérifier le scaling du plafond en 1/(s·T).
**E5 — Pente log-log.** Vérifier la pente −1 de (1 − F(k)) contre k.

Ordre de priorité : E1 > E3 > E4 > E5 > E2. E1 et E3 décident à eux seuls si le papier tient.

---

## 7. Antériorité et positionnement (honnête — à re-vérifier avant soumission)

- **La thèse relationnelle appartient au tournant pragmatique** (van Fraassen 1980 ; De Graaf & Malle 2017 ; Miller 2019 ; Páez 2019). Notre contribution est de la rendre mesurable. L'introduction doit le dire dans les trois premières phrases — sinon desk-reject moral.
- **Le lemme géométrique de l'escalier est folklore-adjacent** : l'inefficacité des coupes axis-parallel sur frontières obliques motive la littérature des arbres obliques (OC1, Murthy et al. 1994). À citer. La nouveauté n'est pas le lemme ; c'est (i) sa lecture récepteur-relative, (ii) la loi sin 2θ comme variable causale d'explicabilité, (iii) le pont statique ↔ interactif [Cor 5.3], (iv) la dichotomie des régimes [Cor 2.3].
- **XAI dialogique** : la compréhension y est mesurée par simulation (arXiv:2408.06960, 2024) mais sans loi de coût ni variable θ ; QC est la métrique qui leur manque.
- **CBM / TCAV** : fournisseurs de V_R et estimateurs de θ — pas des concurrents (Table 3.2).
- **Recherches de sécurisation restantes** (avant soumission) : « query complexity of explanation », « interpretability cost basis rotation », « surrogate fidelity representational alignment » — trois requêtes ciblées pour sécuriser [Cor 5.3] et la loi θ comme inédits.

---

## 8. Verdict de faisabilité et de publiabilité

**Publiable : oui.** Unité minimale, sans le terrain médical :
[T 3.1] + [Table 3.2] (unification) · [T 4.1] + [Cor 4.2] (loi θ : preuve + persistance empirique via Exp 1 ré-analysée) · [P 5.2] + [Cor 5.3] (pont statique ↔ interactif, avec Exp 2 ré-analysée) · [Cor 2.3] (dichotomie, avec diagnostic E3).

**Titre de travail** : « Measuring the pragmatic turn: basis misalignment as a continuous, causal driver of explanation cost ».

**Venue.** Premier choix : TMLR — critères correction + intérêt, pas de course à la nouveauté-spectacle, format adapté à un papier théorie-légère + expériences soignées. Alternatives : XAI World Conference ; AIES/FAccT (moins mathématiques) ; workshop interprétabilité NeurIPS/ICML comme étape. Main track NeurIPS/ICML : seulement avec le terrain médical (papier 2).

**Risques de review et parades.**
R1 « la thèse est connue » → positionnement mesure-du-tournant-pragmatique dès l'abstract.
R2 « le théorème est de la géométrie élémentaire » → citer le folklore, revendiquer la lecture et le Cor 5.3, pas le lemme.
R3 « framework paper, so what » → §6 : cinq prédictions falsifiables testées ; Cor 5.3 : deux mesures unifiées en une loi.
R4 « θ n'est défini que pour des vocabulaires linéaires » → assumé comme problème ouvert [C 1.6b], périmètre explicite.

**Chantiers (4 semaines).**
S1 : preuves propres (lemme de cellule de T 4.1 ; P 2.2 ; version minimax de P 5.2) + Déf 1.6 solide.
S2 : E1–E5 sur le code existant.
S3 : rédaction (structure : intro-positionnement → §1-2 → T 4.1 → Cor 5.3 → expériences → table 3.2 en discussion).
S4 : recherches de sécurisation (§7) + relecture froide.

**Ce qui tuerait le papier** : E1 qui échoue franchement (aucun collapse, déviation sans structure) ; ou une antériorité directe sur le Cor 5.3. Tout le reste est réparable.
