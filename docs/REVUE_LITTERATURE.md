# Revue de littérature — programme REX-Géo (v1, 2026-07-06)

**Méthode** : 5 fronts recherchés en parallèle (workflow, agents avec vérification en
ligne de chaque référence) + 1 sceptique « collision de littérature » sur les preuves.
Toutes les références ci-dessous sont **vérifiées en ligne** (auteurs, année, titre,
venue) sauf mention contraire. Ce document est le livrable de l'issue Linear X-44.

## Résumé stratégique — où est la nouveauté défendable

La relecture adverse a requalifié T1/T2 en faits classiques transposés (voir
`preuves_invariance.md`, sections Positionnement). La carte honnête :

| Élément du programme | Statut littérature | Conséquence |
|---|---|---|
| T1 (invariance du coût, arbres/seuils) | Folklore CART (Breiman et al. 1984) | Citer, transposer à Expl_D |
| T2, d=1 | Connu sous 3 habillages : rangs = invariant maximal (Lehmann-Romano ; Hájek-Šidák) ; FO-définissabilité dans (ℚ,<) (Ryll-Nardzewski + QE de DLO ; Bodirsky & Kára 2008) ; meaningfulness ordinale (Roberts 1979) | Citer frontalement, zéro revendication |
| T2, produit multi-axes, FONCTIONS | Complet : Marichal, Mesiar & Rückschlossová 2005 ; Marichal & Mesiar 2009 (comparison-meaningful functions) ; rangs par composante : Puri & Sen 1971 | Citer |
| T2, produit multi-axes, ÉNONCÉS | **Pas trouvé publié tel quel** (front 1) — mais dérivable du cadre KLST III/Narens | Revendication modeste : « théorème de transfert instancié » |
| **F7 — calcul qualitatif de l'entre-deux/médiane (table de composition, consistance)** | **CHANTIER VIERGE** (front 3 : le survey exhaustif Dylla et al. 2017 ne recense aucun calcul médian) | **Contribution originale candidate n°1** |
| **G3 — superposition ↔ coût pour un récepteur externe** | **PONT OUVERT** (front 5 : les deux moitiés existent séparément, jamais reliées) | **Contribution originale candidate n°2** |
| Conjecture « la langue parle en invariants » (I2/I3) | Convergences fortes (fronts 1, 4) mais jamais formulée ni testée comme loi distributionnelle | **Contribution originale candidate n°3** |
| Le lien Expl(M,R) ↔ invariance ↔ langue ↔ KB | Assemblage inédit | La thèse du papier v2 |

## Front 1 — Théorie de la mesure et meaningfulness

- Stevens, S. S. (1946). On the theory of scales of measurement. *Science* 103(2684), 677-680. — La typologie des échelles par transformations admissibles ; source du choix G = monotones pour l'ordinal.
- Suppes, P. & Zinnes, J. L. (1963). Basic measurement theory. In *Handbook of Mathematical Psychology*, vol. I, 1-76. — Première définition formelle du meaningfulness : significatif ssi invariant sous transformations admissibles — le schéma de [Déf 2.1].
- Krantz, Luce, Suppes & Tversky (1971). *Foundations of Measurement*, vol. I. Academic Press. — Le mesurage conjoint traite les structures produit A₁×A₂×… (notre objet).
- Luce, Krantz, Suppes & Tversky (1990). *Foundations of Measurement*, vol. III. — Le traitement le plus complet du lien invariance ↔ meaningfulness ↔ définissabilité ; cadre de positionnement de T2.
- Roberts, F. S. (1979). *Measurement Theory*. Addison-Wesley (Encycl. of Math. and its Appl., vol. 7). — Meaningfulness appliqué : médiane significative sur ordinal, moyenne non — la moitié classique du Corollaire 2.
- Narens, L. (2002). *Theories of Meaningfulness*. Erlbaum. — Meaningfulness axiomatisé comme invariance/définissabilité, généralisation explicite du programme d'Erlangen.
- Luce, R. D. (1959). On the possible psychophysical laws. *Psych. Review* 66(2), 81-95. — Le type d'échelle contraint la forme des lois : pertinent pour W_cal.
- Orlov, A. I. (1981). *Math. Notes* 30, 774-778 ; Ovchinnikov, S. (1996). Means on ordered sets. *Math. Social Sciences* 32(1), 39-56. — Origines de la comparison-meaningfulness ; Ovchinnikov : sur un ordre **doublement homogène**, les fonctions invariantes continues = polynômes de treillis (min/max/projections).
- **Marichal, Mesiar & Rückschlossová (2005). A complete description of comparison meaningful functions. *Aequationes Math.* 69(3), 309-320** ; Marichal & Mesiar (2009), *Aequationes Math.* 77, 207-236 (state of the art). — L'analogue FONCTIONNEL complet de T2 sous transformations monotones indépendantes par coordonnée.

**Réponse à la question clé** : pas de caractérisation publiée des ÉNONCÉS significatifs
sur produit d'échelles ordinales indépendantes formulée comme T2 ; le cadre pour la
dériver existe (KLST III, Narens). Côté fonctions : complet (Marichal et al.).

## Front 2 — Espaces conceptuels (Gärdenfors)

- Gärdenfors, P. (2000). *Conceptual Spaces: The Geometry of Thought*. MIT Press. — Concepts = régions convexes (critère P), saillance contextuelle par pondération des dimensions.
- Gärdenfors, P. (2014). *The Geometry of Meaning*. MIT Press. — Sémantique lexicale complète par structures géométriques typées.
- Gärdenfors & Williams (2001). Reasoning about categories in conceptual spaces. *IJCAI 2001*, 385-392. — Prototypes + Voronoi : la généralisation à partir de très peu d'exemples vient de la PARAMÉTRISATION par prototypes (k·d réels, dimension VC polynomiale).
- Jäger, G. (2007). *Linguistics and Philosophy* 30(5), 551-564 — les catégories convexes émergent comme stratégies évolutivement stables des jeux de signalisation ; Jäger, G. (2010). Natural color categories are convex sets. *Amsterdam Colloquium 2009*, LNCS 6042. — Preuve empirique World Color Survey (110 langues).
- Hernández-Conde, J. V. (2017). A case against convexity. *Synthese* 194(10), 4011-4037. — LA critique du critère P : la convexité n'est pas stable sous changement de métrique. (Notre réponse : en géométrie ordinale, la classe des boîtes est stable sous G — la critique métrique ne s'applique pas telle quelle.)
- Douven & Gärdenfors (2020). What are natural concepts? *Mind & Language* 35(3), 313-334. — Critère P reformulé en principes de design optimal.
- Bechberger & Kühnberger (2017). A thorough formalization of conceptual spaces. *KI 2017*, LNCS 10505. — Formalisation computationnelle (régions étoilées).
- Steinert-Threlkeld & Szymanik (2019). Learnability and semantic universals. *Semantics & Pragmatics* 12(4). — Les expressions satisfaisant la MONOTONIE sont plus apprenables — l'analogue 1D de la convexité, allié direct de la conjecture.
- **Goyal & Rademacher (2009). Learning convex bodies is hard. *COLT 2009*.** — GARDE-FOU : apprendre un convexe arbitraire exige 2^Ω(√(d/ε)) exemples — la convexité SEULE ne donne pas le few-shot.
- **Sorscher, Ganguli & Sompolinsky (2022). Neural representational geometry underlies few-shot concept learning. *PNAS* 119(43).** — Le théorème quantitatif géométrie ↔ complexité d'échantillon le plus proche (SNR géométrique des variétés de concepts).
- Tětková et al. & Hansen (2025). On convex decision regions in deep network representations. *Nature Communications* 16, 5419. — Convexité approximative pervasive dans les représentations profondes, inspiré de Gärdenfors.

**Réponse à la question clé** : « convexité ⇒ few-shot » est FAUX en général (Goyal-
Rademacher) ; le lien positif est conditionnel — prototypes (VC polynomiale) et SNR
géométrique (Sorscher et al.). Conséquence pour [C 4.5] du noyau : la borne d'échantillon
doit invoquer la paramétrisation par prototypes/boîtes, pas la convexité seule.

## Front 3 — Calculs qualitatifs et algèbres médianes (→ F7)

- Allen, J. F. (1983). *CACM* 26(11), 832-843. — Le gabarit : 13 relations JEPD, table de composition, consistance de chemins.
- Randell, Cui & Cohn (1992). RCC-8. *KR-92*, 165-176. — Le second calcul canonique (régions/connexion).
- Renz & Nebel (1999). *Artificial Intelligence* 108, 69-123. — Le modèle méthodologique : fragments maximaux traitables, consistance en O(n³) — la cible de qualité pour F7.
- Cohn & Renz (2008). QSR. *Handbook of KR*, 551-596 ; **Dylla et al. (2017). A survey of qualitative spatial and temporal calculi. *ACM CSUR*.** — Recensement exhaustif : **aucun calcul de médiane n'existe** ; compositions « faibles » documentées.
- Birkhoff & Kiss (1947). *Bull. AMS* 53(8), 749-752 — l'opération médiane des treillis distributifs ; Bandelt & Hedlíková (1983). Median algebras. *Discrete Math.* 45(1), 1-30 — théorie structurelle, lien médiane ↔ betweenness ; Isbell (1980). *Trans. AMS* 260(2), 319-362 ; Mulder (1980). *The Interval Function of a Graph* — la fonction d'intervalle EST l'entre-deux ; Bandelt & Chepoi (2008). Metric graph theory and geometry: a survey. *Contemp. Math.* — la carte des structures où médiane/entre-deux sont bien définis.
- Précédents partiels à citer et dépasser : Scivos & Nebel (2004), calcul ternaire LR (*Spatial Cognition IV*, LNCS 3343) ; Clementini & Billen (2006), relations projectives ternaires avec « between » (*IEEE TKDE* 18(6)) ; Düntsch, Gruszczyński & Menchón (2023). Betweenness algebras. *J. Symbolic Logic*. — algébrisation modale récente (pas un calcul par contraintes).

**Réponse à la question clé : F7 est essentiellement VIERGE.** Aucun calcul qualitatif
établi (table de composition + théorie de la consistance) pour l'entre-deux, a fortiori
pour la médiane. Trois précédents partiels, aucun ordinal-par-axe. Le corpus des
algèbres médianes fournit la sémantique dénotationnelle gratuite. **Contribution
originale candidate n°1 du programme.**

## Front 4 — Sémantique des comparatifs et typologie (→ conjecture, test multilingue)

- Sapir, E. (1944). Grading: a study in semantics. *Philosophy of Science* 11(2), 93-116. — Le grading précède psychologiquement la mesure : primauté de l'ordinal.
- Klein, E. (1980). A semantics for positive and comparative adjectives. *Linguistics and Philosophy* 4(1), 1-45. — Sémantique du comparatif SANS degrés (délinéation) — le précédent linguistique le plus direct du fragment ordinal.
- Kennedy, C. (2007). Vagueness and grammar. *Linguistics and Philosophy* 30(1), 1-45. — Le camp adverse (degree-based) + contraste relatif/absolu.
- van Rooij, R. (2011). Measurement and interadjective comparisons. *Journal of Semantics* 28(3), 335-358. — Le pont explicite sémantique ↔ théorie du mesurage : significatif au niveau ordinal = invariant sous monotones — quasi-isomorphe à notre lecture.
- Lassiter & Goodman (2017). Adjectival vagueness in a Bayesian model of interpretation. *Synthese* 194. — Le seuil du positif est une inférence pragmatique contextuelle — argument indépendant pour séparer noyau invariant et W_cal.
- Égré & Klinedinst (éds., 2011). *Vagueness and Language Use*. Palgrave. — Le comparatif reste net là où le positif est vague — prédiction directe de la lecture invariantiste.
- **Stassen, L. (1985). *Comparison and Universal Grammar*. Blackwell** ; Stassen (2013). Comparative constructions. *WALS Online*, ch. 121. — 110-167 langues : toutes expriment la comparaison d'inégalité, via 4 stratégies seulement.
- Beck et al. (2009). Crosslinguistic variation in comparison constructions. *Linguistic Variation Yearbook* 9, 1-66. — Ce qui varie entre langues est la machinerie de DEGRÉS, jamais la capacité à exprimer l'ordre.
- **Bochnak, M. R. (2015). The Degree Semantics Parameter. *Semantics & Pragmatics* 8(6).** — Le washo n'a AUCUNE morphologie de degré et exprime la comparaison par juxtaposition : le contenu invariant survit même quand la grammaticalisation échoue.
- Levinson & Meira (2003). 'Natural concepts' in the spatial topological domain. *Language* 79(3), 485-516. — Nuance pour les adpositions : attracteurs statistiques, pas universaux catégoriels.

**Réponse à la question clé — et REFORMULATION IMPOSÉE du test multilingue** :
universalité OUI pour l'EXPRESSIBILITÉ des énoncés d'ordre, NON pour la
grammaticalisation uniforme. Le test multilingue de la conjecture doit être formulé
comme test d'expressibilité (confirmé par la typologie), pas de morphème comparatif
(falsifié par le washo). Les langues « sans degrés » sont l'argument le plus fort :
elles réalisent presque à l'état pur le fragment invariant, sans couche de calibration.

## Front 5 — Interprétabilité et représentation (→ G3, KB)

- Elhage et al. (2022). Toy models of superposition. *Transformer Circuits Thread*, arXiv:2209.10652. — La superposition : prémisse du pont G3.
- Scherlis et al. (2022). Polysemanticity and capacity in neural networks. arXiv:2210.01892. — LA mesure du degré de superposition (capacité par feature) : la moitié « émetteur » de G3.
- **Ayonrinde, Pearce & Sharkey (2024). Interpretability as compression (MDL-SAEs). arXiv:2410.11179.** — Le travail le plus proche de G3 : interprétabilité = coût de communication en bits vers un récepteur. **Risque de collision principal** — différenciateur : notre récepteur parle le fragment invariant ordinal, pas un code de features ; et G3 vise une LOI superposition ↔ coût, pas une métrique de description.
- Adler & Shavit (2024). On the complexity of neural computation in superposition. arXiv:2409.15318. — Bornes de complexité du calcul en superposition (côté réseau, pas côté récepteur).
- Higgins et al. (2018). Towards a definition of disentangled representations. arXiv:1812.02230. — Disentanglement par groupes de symétries : le parallèle formel le plus proche (produit de facteurs, groupe d'invariance) — sans ordinalité, sans T2, sans langue.
- Koh et al. (2020). Concept bottleneck models. *ICML 2020*. — Interface de concepts nommés, plate et sans géométrie.
- Olah et al. (2020). Zoom in: circuits. *Distill*. — L'approche opposée (inspection interne) ; REX définit un critère côté récepteur, indépendant du substrat.
- Petroni et al. (2019). Language models as knowledge bases? *EMNLP 2019* ; Sun et al. (2024). Head-to-tail. *NAACL 2024*. — Le rappel paramétrique des LLM est réel mais non fiable (queue de distribution) : motivation quantitative de la KB requêtable.

**Réponse à la question clé : le pont G3 n'a jamais été établi.** Ses deux moitiés
existent (Scherlis : mesure de superposition ; Ayonrinde : coût de communication d'une
explication) mais aucune loi ne les relie, et personne ne le fait dans un langage
d'invariants ordinaux. **Contribution originale candidate n°2.**

## Références issues du sceptique « collision » (à citer dans les preuves)

Lehmann & Romano, *Testing Statistical Hypotheses* (invariant maximal = rangs) ;
Hájek & Šidák, *Theory of Rank Tests* ; Puri & Sen (1971), *Nonparametric Methods in
Multivariate Analysis* (rangs par composante) ; Bodirsky & Kára (2008), *STOC*
(FO-définissabilité dans (ℚ,<)) ; Bodirsky, Martin & Mottet (2018), *JACM* (CSP
temporels discrets — pour L4) ; Breiman, Friedman, Olshen & Stone (1984), *CART*
(folklore d'invariance monotone) ; Glass, *Ordered Permutation Groups* (chaînes
doublement homogènes — le bon cadre pour T2).

## Prochaines actions de littérature

1. Vérifier le chapitre exact de KLST vol. III et Narens 2002 où le pont
   invariance↔définissabilité est établi (citations de précision pour T2).
2. Typologie de l'ordre temporel (« avant/après ») : non couverte par ce lot — pistes
   Hetterle, Cristofaro (clauses adverbiales), à compléter avant le test multilingue.
3. F7 : lire Bandelt & Hedlíková 1983 et Dylla et al. 2017 en entier avant de
   construire la table de composition.

## Complément v1.1 (intégration de l'étude complémentaire, 2026-07-06)

Nouvelles références vérifiées à intégrer au corpus (voir `preuves_invariance.md` v0.3
et `I1_grammaire_fragment_invariant.md`) :
- **Dushnik & Miller (1940)**, Bull. AMS 46 — chaînes rigides denses dans ℝ (le
  contre-exemple qui impose (H)).
- **Copules** : Sklar ; Schweizer & Wolff (1981), Ann. Statist. 9 ; Nelsen (2006),
  *An Introduction to Copulas* §2.4 ; Genest & Nešlehová (2007), ASTIN 37 (atomes, L1′).
- **Communication sans calibration commune** : Juba & Sudan (2008), STOC — la maison
  méthodologique de la version forte de la conjecture, avec Kemp & Regier (2012),
  Science, et Steinert-Threlkeld & Szymanik (2020), Cognition (universaux par
  efficacité).
- **Corpus du pilote F3** : Camburu et al. (2018), e-SNLI, NeurIPS ; Rajani et al.
  (2019), CoS-E, ACL ; Wang (2017), LIAR, ACL ; Alhindi et al. (2018), LIAR-PLUS,
  FEVER@EMNLP.
- **Complexité (complète la session 11)** : van Beek (1992), Artif. Intell. 58
  (algèbre de points polynomiale) ; Garey & Johnson (1979), entrée « Betweenness ».
- Sémantique des degrés, ajout : Sassoon (théorie de la mesure en sémantique) — à
  vérifier précisément avant citation.
