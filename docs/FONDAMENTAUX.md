# Fondamentaux — clarification de l'intuition initiale

**Document vivant. Juge de paix de tout design d'expérience futur.**
Méthode : Reda énonce l'intuition avec ses mots ; l'assistant joue l'avocat du diable ;
on note ce qui survit. Aucune expérience n'est conçue tant que ce document ne la force pas.

---

## Session 1 (2026-07-06) — « Qu'est-ce qui se passe quand quelqu'un dit "ah d'accord" ? »

### Énoncé brut (Reda)

> Quand on parle, on cherche une base commune, mais cette base commune doit être construite
> de chaque côté par une boucle rétroactive. Plusieurs politiques possibles : on peut
> accepter, challenger par rapport aux croyances personnelles, vérifier la logique, en
> procédure logique entre éléments matchant de la connaissance. Et donc plusieurs dynamiques
> mesurables émergent. Quand on dit « ah d'accord », ça peut être une contre-vérification
> qui trouve une cohérence non attendue, et qui modifie violemment le graphe projeté
> (car personnel) commun de connaissance. Le commun dépend d'un contexte ; il y a toujours
> un contexte ; c'est même le nerf de la guerre, car il définit peut-être aussi la base.

### Concepts nommés (raffinage minimal)

1. **La base commune est construite, pas donnée** — produit du dialogue par boucle
   rétroactive bilatérale. Renversement du cadre actuel où R = (V_R, C_R) est statique.
2. **Projection personnelle du commun** : il n'existe pas de graphe commun ; chaque agent
   tient Ĝ_soi(commun). La conversation couple les projections. (Ancrages à vérifier pour
   le papier : common ground — Clark ; Stalnaker ; grounding in communication.)
3. **Politiques de mise à jour π** : accepter / challenger contre croyances / vérifier la
   logique / matcher procéduralement. R devient (V_R, C_R, π_R). Chaque π engendre une
   dynamique mesurable. L'Exp 2 n'a mesuré que π = accepter.
4. **« Ah d'accord » = contre-vérification trouvant une cohérence inattendue → mise à jour
   VIOLENTE (non locale, en cascade) de la projection.** Définition opératoire de l'insight.
5. **Le contexte est omniprésent et définit peut-être la base** — le nerf de la guerre.

### Attaques d'avocat du diable (ouvertes, à trancher)

- **A1 — Le problème du snapshot** : si la base se construit, Expl(M, R, ε) à vocabulaire
  fixe est une photo d'un processus dont la grandeur réelle est la trajectoire. Candidat de
  généralisation : le coût pour amener deux projections à coïncider « assez pour le
  contexte » ; la courbe d'explicabilité en serait la section instantanée. Les Exp 1-7
  survivent-elles comme cas limite statique ? [à trancher par Reda]
- **A2 — La violence contre le zéro-oubli** : le canal humain a deux modes — patch local
  (garanti sans régression) et restructuration en cascade (l'insight, non locale). Le moteur
  actuel n'implémente que le premier. **Frontière sûreté/insight** : trade-off fondamental
  candidat du paradigme. Qui contrôle le curseur — la politique π ? [ouvert]
- **A3 — Le contexte : réductible ou primitif ?** Lecture faible : κ = (Q̄, ε, sous-graphe
  actif) — se réduit au cadre existant. Lecture forte : le contexte engendre le vocabulaire
  lui-même — primitif irréductible, trou dans le cadre actuel. **Test décisif** : exhiber un
  cas vécu où, entre les deux mêmes personnes à connaissances égales, le changement de
  contexte change non pas les questions mais LES CONCEPTS DISPONIBLES. [question posée à Reda]

### Grandeurs mesurables identifiées

- Vitesse de convergence des projections, par politique π.
- Distribution des tailles de mise à jour ; l'insight = queue lourde (événement rare et gros).
- Coût (en tours) pour atteindre la cohérence contextuelle.
- Asymétrie des trajectoires : qui bouge, M ou R ?
- Continuité avec l'existant : Exp 2 (une politique, base fixe) et Exp 7 (patchs locaux
  cumulés) sont des points de cet espace.

### Prochaine question de la séance

Le test décisif de A3 : un exemple vécu où le contexte a changé les concepts disponibles,
pas seulement les questions posées.

---

## Session 2 (2026-07-06) — Le flou du langage et la superposition de graphes

### Énoncé brut (Reda)

> Il faut qu'on introduise une logique de flou pour les qualifications du langage, mais
> dans un graphe qui joue uniquement avec les caractéristiques naturelles des graphes.
> Note qu'on peut avoir une superposition de graphes.

### Formulation raffinée

**Le flou = une mesure sur des graphes nets.** Un prédicat flou (« grand », « proche »)
n'est pas un nœud flou : c'est une population de graphes nets ne différant que par leurs
seuils. μ(x) = fraction de la superposition qui classe x. Version minimale : un graphe
unique à **seuils-intervalles** (taille > θ, θ ∈ [a, b]) — la fonction d'appartenance de
Zadeh est l'ombre projetée d'un ensemble de graphes nets. Rien d'importé : annotation
native du graphe, localité de W⁻¹ préservée.

### Ce que ça referme (liens avec la session 1)

1. **L'état de la boucle rétroactive** : une projection du commun à mi-convergence EST une
   superposition — le dialogue ne transporte pas un graphe, il rétrécit une mesure.
2. **Mécanisme du « ah d'accord » (réponse partielle à A2)** : l'insight = effondrement de
   la superposition (chute d'entropie en un tour, mesurable). La frontière sûreté/insight
   devient un paramètre continu tenu par la politique π : combien d'effondrement une phrase
   a le droit de déclencher.
3. **Faiblesse de l'Exp 7 réglée en principe** : une phrase floue (« quand c'est grand,
   refuse ») n'engage pas sur un seuil faux — elle installe l'intervalle compatible avec
   l'usage du mot ; les tours suivants le rétrécissent. Le flou cesse d'être du bruit :
   c'est la sémantique exacte de la phrase.

### Garde-fous de lucidité (actés)

- **Piège de la forêt** : superposition non contrainte = random forest = boîte noire
  recréée. Contrainte : squelette partagé ; l'incertitude ne porte que sur les paramètres
  (seuils, classes) et localement sur la structure. C'est le sens de « uniquement les
  caractéristiques naturelles des graphes ».
- **Traduisibilité** : W sur une superposition rend le chemin consensuel + le lieu
  d'ambiguïté (« gros, ici, ça commence entre 10 et 14 k€ ») — jamais une distribution
  illisible, sinon l'axiome de traduisibilité tombe.
- **Vocabulaire** : « superposition » au sens mesure sur des structures ; pas de
  connotation quantique dans le papier.
- **Discipline** : rien n'est codé ; l'idée doit survivre aux attaques comme le reste.

### Grandeurs mesurables ajoutées

- Entropie de la superposition au fil des tours = LA courbe de convergence de la session 1.
- Insight = discontinuité d'entropie (queue lourde de la distribution des mises à jour).
- Largeur des intervalles de seuils = incertitude sémantique résiduelle par concept.

### Question ouverte de la session 2

**La question de calibration est-elle un nouvel opérateur ?** Quand on dit « les gros
dossiers, refuse-les » et qu'un cas limite arrive, l'humain demande : « et 12 000 €,
c'est gros ? ». Est-ce (a) un troisième opérateur W_cal (requête de frontière), ou
(b) un W contrastif sur une paire minimale (« pourquoi 12 000 serait gros et 11 000 non ? »),
donc réductible au cadre existant ? [posée à Reda]
