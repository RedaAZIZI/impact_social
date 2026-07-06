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
donc réductible au cadre existant ?

**Position de Reda : il y a quelque chose dans (a).** Indice retenu : la réponse humaine
(« bof, à la limite ») est une lecture directe de μ, qu'aucun des deux opérateurs
existants ne rend.

---

## Session 3 (2026-07-06) — Quatre expériences pour mettre W_cal en danger

Conçues pour attaquer (a), pas pour le confirmer. Coût zéro (pensée pure ou synthétique
sans API). Ordre recommandé : E2 → E4 → E1 → E3 (les in-silico attendent la fin du recul).

- **E1 — Le jeu du douanier** (pensée → in-silico). Enseignant à seuil net, apprenant à
  superposition. Trois protocoles : W seul / W-contrastif (bissection, O(log 1/δ)) /
  W_cal (lectures de μ). Mesure : tours pour rétrécir l'intervalle à δ. **La vraie
  question : à quel niveau de grossièreté des réponses μ (l'humain rend 3-5 niveaux, pas
  des décimales) l'avantage de W_cal s'effondre-t-il ?** Un opérateur mérite le statut de
  primitif si son avantage de complexité de requête est robuste au bruit humain. Branche
  sur la Proposition 2 (hiérarchie d'opérateurs ordonnée par complexité de requête, pont
  Angluin).
- **E2 — Le type de retour** (pensée pure, rendement conceptuel maximal). Réponses humaines
  observées à « c'est gros, 12 000 ? » : (1) lecture graduée ; (2) recalibrage par exemple
  (« gros c'est plutôt 20 000 ») ; (3) renvoi au contexte (« ça dépend »). Les formes (2)
  et (3) sont des ÉDITIONS de la superposition du demandeur, pas des explications.
  **Test décisif : trouver une réponse de calibration qui ne soit pas une édition.**
  Si impossible → W_cal est le point fixe de la dualité W/W⁻¹ — l'endroit où le canal de
  lecture et le canal d'écriture coïncident. Candidat au plus beau théorème informel du
  papier.
- **E3 — Le pont vers le contexte** (relie sessions 1 et 2). Hypothèse : les réponses de
  calibration forkent selon le contexte bien plus que les réponses de justification —
  W rend la même règle dans deux contextes, W_cal rend deux seuils. Si ça tient, W_cal est
  **l'instrument de mesure qui rend le contexte observable** : l'attaque A3 devient
  empiriquement testable au lieu de rester un débat.
- **E4 — La calibration silencieuse** (l'avocat du diable contre (a)). L'intervalle se
  rétrécit passivement par l'usage, sans question (les enfants apprennent « grand » sans
  demander la frontière). Objection : W_cal = accélération explicite d'une calibration
  ambiante, pas un opérateur. **Test : existe-t-il une information que W_cal obtient et
  qu'aucune observation passive ne peut obtenir ?** Candidat : la frontière dans les zones
  rares (où les exemples ne tombent jamais). Si oui, (a) survit.

---

## Session 4 (2026-07-06) — Le codage est le langage : embedding à la frontière et croissance du graphe

### Énoncé brut (Reda)

> Le codage est le langage, donc je pense qu'il faut introduire une notion d'embedding du
> texte dans le graphe, ou l'agrandir si besoin — je pense qu'il manque cette partie.

Contexte déclencheur : test réel du labo conversationnel — la phrase « rien n'est jamais
faux, sauf quand l'ego ou la peur interviennent » est tombée hors du vocabulaire (le
lexique à mots-clés est un embedding artisanal et pauvre) ; « ego » et « peur » n'existent
pas dans V_R.

### Formulation raffinée — l'architecture en deux moitiés

1. **Le transducteur (texte → V_R)** : une fonction E qui projette le texte libre sur les
   concepts existants du graphe. C'est la porte d'entrée de la langue. Le lexique actuel
   du labo en est la version minimale ; la version réelle = un encodeur (embedding ou LLM).
2. **Le détecteur de croissance (le résidu)** : ce que E ne peut PAS projeter sur les
   concepts existants — le résidu — est le signal d'agrandissement. Quand les résidus de
   plusieurs messages s'alignent (beaucoup de phrases parlent d'« ego », de « peur »),
   cette direction est candidate à la promotion en **nouveau concept nommé** du graphe.
   Mécanisme candidat pour [C 1.6b] (extension de vocabulaire) et pour l'item 6 de la
   roadmap (édition non exprimable dans le vocabulaire partagé).

### Le garde-fou décisif (lucidité)

**L'embedding vit à la frontière, jamais dans le graphe.** Les nœuds restent des prédicats
nets sur des concepts NOMMÉS ; le vecteur continu ne sert qu'à (a) transduire et
(b) détecter les résidus. Si des vecteurs entrent dans les nœuds, on a réimporté la boîte
noire que le cadre combat. Corollaire : la promotion d'un résidu en concept passe par un
**acte de nommage** (par l'humain, ou proposé puis validé) — c'est le moment où une
direction devient un mot, c'est-à-dire exactement « la langue converge au niveau de ce
référentiel » (Reda, création du labo) et le « ah d'accord » de la session 1 côté
vocabulaire. Lien littérature : CBM = fournisseurs de V_R appris (table 3.2 du noyau
formel) ; ici, un CBM **construit par le dialogue** plutôt qu'à l'entraînement.

### Conséquence architecturale immédiate

Le programme REX-LLM (en pause) trouve ici son point d'entrée motivé par l'usage : le LLM
non pas comme objet à distiller d'abord, mais comme **transducteur + détecteur de
croissance** du labo — « projette ce texte sur ces six concepts ; liste les concepts
présents dans le texte que ces six ne couvrent PAS ». Le résidu revient déjà nommé.
Coût : centimes par message. Aucun vecteur n'entre dans le graphe.

### Questions ouvertes de la session 4

- Qui nomme ? (l'humain seul / le LLM propose et l'humain valide / seuil de résidus
  récurrents avant proposition) — la politique de nommage est une politique π de plus.
- Quand un concept est promu, comment les règles existantes l'adoptent-elles ?
  (superposition, session 2 : le nouveau concept entre avec des seuils-intervalles larges,
  rétrécis par le dialogue.)
- Critère de refus de croissance : quand faut-il NE PAS agrandir (concept redondant,
  résiduel exprimable comme combinaison des existants) ?

---

## Session 5 (2026-07-06) — « Les concepts sont des formes » : le tournant géométrique

### Énoncé brut (Reda)

> Notre graphe minimal est géométrique, et tout le langage construit une réalité
> géométrique. Cette réalité est décrite par les formes des concepts : les concepts ne
> sont pas des vecteurs, ce sont des formes dans des géométries — parfois riemanniennes.
> Il faut encoder l'information de façon géométrique, ou que le réseau de neurones
> reflète cette géométrie — pas de façon random où les concepts sont mélangés et où on
> finit par approximer. On veut quelque chose d'explicable, de programmable, et un
> apprentissage qui nécessite très peu de données. Une vraie intelligence, même sans
> connaître une langue, va associer des formes géométriques déjà acquises aux nouveaux
> symboles que sont cette langue.

### Formulation raffinée — la vision n'est pas un fork, c'est la théorie latente des Exp 1-7

1. **Un concept n'est déjà pas un vecteur dans le cadre : c'est une région.** Une règle
   « revenu > 20k ∧ durée < 12 » est une boîte alignée aux axes — une région convexe
   NOMMÉE de l'espace des qualités. RuleListModel = une partition de l'espace en formes
   nommées. La superposition (session 2) = une forme à frontière épaisse ; μ en est
   l'ombre. Le cadre parlait déjà géométrie sans le dire.
2. **Le programme d'Erlangen de l'explicabilité.** Klein (1872) : une géométrie EST un
   groupe d'invariances. L'Exp 1b a identifié empiriquement le groupe d'invariance du
   coût d'explicabilité : les homéomorphismes monotones coordonnée-par-coordonnée. Ce qui
   coûte, c'est ce qui casse le groupe — le mélange, les rotations. Relecture : **le
   vocabulaire du récepteur définit une géométrie (au sens de Klein) ; expliquer, c'est
   décrire les formes de décision de M dans l'atlas de R ; le coût d'explicabilité est un
   invariant géométrique du couple (formes de M, atlas de R).** Prop 1 devient un théorème
   de groupe d'invariance ; [C 4.3] (angles principaux) devient la quantification du
   défaut d'alignement entre atlas.
3. **Ancrages littérature (à vérifier pour le papier).** (a) Gärdenfors, *Conceptual
   Spaces* : les concepts naturels = régions CONVEXES d'espaces de qualités ; la convexité
   explique l'apprentissage à très peu d'exemples (prototype + cellules de Voronoi) — le
   « very little data » de l'énoncé a déjà son théorème candidat. (b) Elhage et al. 2022,
   *Toy Models of Superposition* : les réseaux réels mélangent les concepts dans des
   directions non alignées — le « pas de façon random où les concepts sont mélangés » de
   l'énoncé est exactement la superposition de l'interprétabilité mécaniste, et l'Exp 1
   mesure ce que ce mélange coûte au récepteur. Pont inédit candidat. (c) Geometric deep
   learning (Bronstein et al.) : concevoir l'architecture par ses invariances — allié sur
   « le réseau doit refléter la géométrie ». (d) Higgins et al. : désenchevêtrement défini
   par les symétries.
4. **La « vraie intelligence » de l'énoncé = le transducteur de la session 4, côté
   géométrie.** Apprendre une langue nouvelle = apparier des symboles neufs à des formes
   déjà acquises. Peu de données parce que les formes portent déjà toute la structure —
   il ne reste qu'un problème d'appariement, pas un problème d'apprentissage. C'est
   falsifiable (G2 ci-dessous).

### Attaques d'avocat du diable

- **A-G1 — Le piège de la poésie.** « Forme » et « géométrie » sont des mots séduisants
  et infalsifiables tant qu'on ne fixe pas le groupe d'invariance. Règle actée : toute
  affirmation géométrique du papier doit se réduire à un invariant MESURABLE. Et
  lucidité : la géométrie démontrée aujourd'hui est **ordinale** (produit de dimensions
  ordonnées) — « riemannien » reste en perspective tant qu'aucun résultat n'exige la
  courbure. Pas dans le titre.
- **A-G2 — Réimporter la boîte noire.** Si les formes deviennent des surfaces implicites
  apprises librement par un réseau, on a recréé ce que le cadre combat. Contrainte (même
  garde-fou que session 4) : les formes restent des objets NOMMABLES — boîtes, régions
  convexes dont les directions de faces sont des concepts nommés. Un concept composé
  (« ratio dette/revenu ») = une nouvelle direction nommée = agrandir l'atlas ; c'est
  exactement le vocabulaire ingénieur de l'Exp 6.
- **A-G3 — Nouveauté réelle ou relecture ?** Réponse honnête : une relecture — mais une
  relecture qui remplit précisément le trou théorique du papier v1. Rien des Exp 1-7
  n'est perdu ; tout se relit et se renforce.

### La décision (papier refusé vs nouvelle direction) — position de l'assistant

**Ni forcer la resoumission telle quelle, ni fork : le tournant géométrique EST la v2.**
Le reproche type fait à un position paper (« un cadre + des jouets synthétiques, où est
la théorie ? ») est exactement ce que le noyau géométrique répond. Thèse v2 candidate :
*l'explicabilité est un problème de changement d'atlas ; son coût est un invariant
géométrique du couple (M, R)*. Les 7 expériences deviennent les mesures de cet invariant.

### Programme G (in-silico, coût quasi nul, aucun code tant que non forcé par ce doc)

- **G1 (théorie)** : prouver Prop 1 comme théorème de groupe d'invariance (les arbres à
  seuils ne dépendent que des ordres) ; attaquer [C 4.3] — le coût comme fonction des
  angles principaux entre les atlas.
- **G2 (le test de la vraie intelligence — symbol grounding)** : deux apprenants, mêmes
  données ; l'un possède une bibliothèque de formes acquises, l'autre est tabula rasa ;
  on présente une « langue » nouvelle (symboles renommés/permutés). Mesure : ratio de
  complexité d'échantillon pour ancrer les symboles à fidélité ε. **Critère de
  falsification : si le tabula rasa fait aussi bien, les formes n'apportent rien.**
- **G3 (le pont interprétabilité)** : réseaux jouets entraînés avec/sans pression
  d'alignement (désuperposition). Prédiction : la courbe d'explicabilité suit le degré de
  superposition mesuré (angles principaux entre features et axes). Relie REX à Elhage
  et al. 2022 — et donne un contenu opératoire à « le réseau doit refléter la géométrie ».

### Grandeurs mesurables ajoutées

- Ratio de complexité d'échantillon avec/sans formes acquises (G2) — LA mesure du
  « very little data ».
- Degré de mélange (angles principaux) ↔ coût d'explicabilité (G1/G3) : la loi
  quantitative candidate du cadre.
- Taille de description d'une forme de M dans l'atlas de R à ε fixé — le coût
  d'explicabilité relu comme complexité géométrique de description.

### Questions ouvertes de la session 5

- Où la courbure devient-elle NÉCESSAIRE ? (candidat : similarité perçue non euclidienne,
  motivée par Gärdenfors — mais exiger un résultat qui la force avant de l'introduire.)
- La langue construit-elle la géométrie ou la révèle-t-elle ? (version géométrique de
  l'attaque A3-contexte, session 1 — l'énoncé brut penche pour « construit ».)
- Statut des formes non convexes (concepts disjonctifs : « acceptable sauf si ») —
  frontière du critère P de Gärdenfors, et lieu probable où la liste de règles bat la
  région convexe unique.

---

## Session 6 (2026-07-06) — Les relations sont géométriques ; la langue parle en invariants

### Énoncé brut (Reda)

> Si je dis « je suis plus puissant que lui », ça veut dire juste que le concept puissance
> chez moi, cette propriété, a un volume plus grand — peut-être, ou selon une certaine
> projection. Il y a toujours un parallèle géométrique à ce dont on parle. Et ça se voit
> surtout dans les relations entre les objets : un truc DANS un truc, un truc AVANT un
> truc. Et je pense que ce ne sont même pas des formes stables : des formes qui tournent
> autour de certains attracteurs, comme des ondes, qui ont des états, qui changent d'état
> continuellement, de façon fréquentielle. Peut-être qu'on va chercher juste un truc
> statique d'abord — on verra comment on va gérer ça, mais je le dis.

### Formulation raffinée

1. **La sémantique relationnelle est géométrique ET nommable.** « Plus puissant que » =
   dominance ordinale le long d'une direction nommée ; « dans » = inclusion de régions ;
   « avant » = précédence d'intervalles. Point décisif : les calculs qualitatifs existants
   sont des ensembles FINIS de relations nommées — RCC-8 (Randell, Cui & Cohn 1992 :
   8 relations spatiales entre régions), algèbre d'Allen (1983 : 13 relations temporelles
   entre intervalles). Finis, discrets, composables : natifs pour un graphe, traduisibles
   par W. Ancrages : Gärdenfors *The Geometry of Meaning* (2014) ; schémas-images de
   Lakoff & Johnson (contenance, chemin, force).
2. **L'inclusion de régions EST l'implication logique.** A ⊆ B ⟺ (x ∈ A ⇒ x ∈ B). Le pont
   formes ↔ graphe n'est pas une analogie, c'est une identité : les hiérarchies de
   subsomption sont des emboîtements de formes. Les arêtes du graphe minimal peuvent
   PORTER les relations géométriques qualitatives — « uniquement les caractéristiques
   naturelles des graphes » (session 2) reste respecté.
3. **Les comparatifs vivent dans la géométrie déjà démontrée.** « Plus X que » n'exige
   qu'un ordre le long d'une projection nommée — exactement le fragment préservé par le
   groupe d'invariance identifié en Exp 1b (déformations monotones coordonnée-par-
   coordonnée). Aucune courbure requise.
4. **Conjecture « la langue parle en invariants » (candidate au cœur de la v2).** Les
   déformations monotones ne préservent NI les coordonnées absolues NI les distances —
   elles préservent les ordres, les inclusions, les précédences. Or le langage qualitatif
   naturel parle précisément en comparatifs, inclusions et précédences. Lecture : chaque
   locuteur tient une base qui est une déformation monotone inconnue de celle de l'autre ;
   la langue a convergé vers le fragment qui se transfère sans connaître la déformation —
   **les invariants du groupe**. Corollaire qui referme la session 2/3 : W_cal existe
   parce que les comparatifs sous-déterminent les seuils — la calibration est le moment
   précis où la langue doit SORTIR du fragment invariant pour épingler une frontière
   absolue. L'opérateur n'est plus une curiosité : c'est la porte de sortie du fragment.
5. **« Selon une certaine projection » = lecture géométrique du contexte (attaque A3).**
   « Plus grand » en hauteur ou en volume : la dominance ne tient que sous une projection,
   et c'est le contexte qui choisit la projection. Candidat de résolution de A3 : le
   contexte ne change pas les concepts, il change la SECTION des formes qu'on regarde —
   ce qui expliquerait que les réponses de calibration forkent selon le contexte (E3)
   pendant que les règles restent stables.
6. **La dynamique (attracteurs, ondes) — squelette discret déjà en place.** La
   superposition (session 2) est la photo instantanée d'un état ; le contexte est le
   sélecteur d'attracteur ; l'insight (session 1) est la transition d'état. Décision
   alignée avec l'énoncé de Reda lui-même : statique d'abord, la dynamique entre par une
   seule mesure (ci-dessous), pas par un formalisme.

### Attaques d'avocat du diable

- **A-G4 — Le piège des ondes.** « Ondes », « fréquentiel » : la partie la plus poétique
  de l'énoncé ; aucun phénomène mesuré n'exige aujourd'hui une dynamique oscillatoire.
  Règle actée : le mot « onde » n'entre dans aucun document public tant qu'une mesure ne
  montre pas de récurrence d'états. Opérationnalisation minimale : un concept sondé par
  W_cal à travers contextes et temps montre-t-il (a) un petit ensemble d'états récurrents
  (attracteurs), (b) une dérive continue, (c) du bruit ? Testable dans le labo
  conversationnel, coût nul. Reda a lui-même fourni le garde-fou (« peut-être un truc
  statique d'abord ») — acté.
- **A-G5 — Les relations : primitives ou sucre syntaxique ?** « Dans », « avant »,
  « plus que » sont réductibles à des prédicats sur coordonnées, donc pourquoi des
  primitives ? Réponse d'Erlangen : en tant que FAITS, réductibles ; en tant que
  VOCABULAIRE, ce sont les seuls énoncés qui se transfèrent entre bases déformées. Leur
  statut de primitive vient de la traduisibilité, pas de l'expressivité.
- **A-G6 — L'explosion relationnelle.** Ajouter des relations peut faire exploser le
  langage du graphe (paires, triplets d'objets). Garde-fou : calculs FINIS uniquement
  (RCC-8 : 8, Allen : 13, dominance : 3 par projection nommée) — énumérables, nommables,
  pas de relation apprise librement.

### Grandeurs mesurables ajoutées

- **Fraction invariante du langage d'explication** : part des énoncés humains
  d'explication exprimables dans le fragment (comparatifs, inclusions, précédences) vs
  exigeant une valeur absolue. Prédiction de la conjecture : dominance massive du
  fragment invariant, et les sorties du fragment coïncident avec les moments de
  calibration (W_cal). Testable sur corpus.
- **Récurrence d'états d'un concept** : nombre d'états distincts de μ par concept à
  travers contextes/temps, et leur taux de retour — attracteurs si petit et récurrent,
  dérive si non (tranche A-G4).
- **Pouvoir de compression des relations** : taille d'explication en relations
  qualitatives vs en prédicats à seuils, à fidélité égale.

### Questions ouvertes de la session 6

- La conjecture « la langue parle en invariants » : test corpus réaliste ? (fréquence des
  comparatifs vs absolus dans des explications humaines réelles ; les absolus
  apparaissent-ils surtout en position de calibration ?)
- W sur une relation : à quoi ressemble « pourquoi A avant B ? » — l'espace des réponses
  est-il le même que pour « pourquoi A ∈ classe X ? » (les relations vivent sur des paires,
  donc dans un espace produit) ?
- Si les attracteurs existent, qui les tient : le concept, le contexte, ou la politique π ?

---

## Session 7 (2026-07-06) — La conjecture devient le fer de lance ; la force humaine synthétique industrielle

### Énoncé brut (Reda)

> La première [la conjecture « la langue parle en invariants »] est ma préférée. Ça semble
> très ambitieux, et avec la force humaine synthétique industrielle (la disponibilité des
> API et le multi-requêtage de l'IA), on peut construire une théorie solide qui conçoit un
> produit qu'on pourra développer, car on pourra entraîner, requêter ou maintenir un
> graphe avec des millions de paramètres.

### Décision

**La conjecture « la langue parle en invariants » (session 6, point 4) devient le fer de
lance théorique de la v2 du papier.** Les tournants géométrique (session 5) et relationnel
(session 6) s'y subordonnent : la géométrie fournit le groupe, les relations fournissent le
fragment, la conjecture fournit la thèse.

### Formulation raffinée

1. **« La force humaine synthétique industrielle » = une primitive méthodologique
   nouvelle.** Les API de LLM au multi-requêtage rendent industrielles des expériences qui
   exigeaient hier des cohortes humaines : annotation de corpus à l'échelle, dialogues
   synthétiques pré-enregistrés, juges multiples indépendants (modèles/températures
   différents) avec accord inter-annotateurs mesuré. Coût : centimes par jugement.
2. **La distinction d'usage qui rend ça valide (garde-fou constitutif).** Deux usages très
   différents : (a) **le LLM comme corpus** — il mesure des propriétés DE LA LANGUE (sa
   distribution d'énoncés) ; (b) **le LLM comme sujet synthétique** — il mesure le modèle,
   pas l'humain. Chance structurelle : la conjecture porte sur la langue, pas sur la
   cognition — elle relève du cas (a), le cas défendable.
3. **La chaîne théorie → produit, explicitée.** Si la langue parle en invariants, alors le
   canal de maintenance d'un graphe (des phrases) est robuste aux déformations de base
   entre mainteneurs — c'est POURQUOI 1 phrase > 3000 exemples (Exp 3, Exp 7), et pourquoi
   un graphe à millions de paramètres reste maintenable par dialogue : **le fragment
   invariant est l'API du produit**, et W_cal traite le résidu borné (les moments où il
   faut épingler un absolu). La théorie ne décore pas le produit : elle en est la garantie
   de maintenabilité.
4. **Le graphe à millions de paramètres, précisé.** Paramètres = seuils nommés +
   intervalles de superposition + structure — jamais des poids anonymes. « Entraîner »
   (données), « requêter » (W), « maintenir » (W⁻¹ / W_cal). La question d'échelle
   centrale : la localité de l'édition (Exp 7, invariant de /tests) survit-elle à 10⁶
   paramètres ? C'est exactement le palier 5 d'Exp 8 (accrétion de contextes).

### Programme I (invariants) — industriel, pré-enregistré, palier par palier

- **I1 (théorie, coût nul, PRÉREQUIS BLOQUANT)** : grammaire formelle du fragment
  invariant — comparatifs, inclusions, précédences, qualificatifs monotones — vs énoncés
  absolus (valeurs, unités, seuils). Sans I1, aucun appel API : on ne compte pas ce qu'on
  n'a pas défini.
- **I2 (corpus, centimes)** : fraction invariante dans des explications humaines RÉELLES
  (pas générées) ; annotation LLM multi-requêtée, plusieurs juges indépendants, accord
  inter-annotateurs rapporté.
- **I3 (la prédiction tueuse)** : dans les dialogues, les sorties du fragment (énoncés
  absolus) co-occurrent avec les moments de calibration. **Falsification : si les absolus
  sont distribués uniformément dans le dialogue, le corollaire W_cal tombe.**
- **I4 (pont produit)** : part de la maintenance d'un graphe exprimable dans le fragment
  invariant seul ; le résidu mesure le besoin de W_cal. Se branche sur Exp 8 palier 5.

### Attaques d'avocat du diable

- **A-G7 — La circularité.** Tester « la langue parle en invariants » avec des juges qui
  SONT des produits statistiques de la langue. Tranché par la distinction d'usage : valide
  tant que la conjecture porte sur la distribution des énoncés de la langue ; invalide dès
  qu'on en tirerait une conclusion sur la cognition humaine. Frontière à écrire noir sur
  blanc dans le papier.
- **A-G8 — L'échelle n'est pas la solidité.** Un million de requêtes donne de la puissance
  statistique, pas de la validité conceptuelle. D'où I1 bloquant, et la discipline Exp 8
  intégralement maintenue : pré-enregistrement, go de Reda palier par palier, budget
  plafonné.
- **A-G9 — Le produit trop tôt.** STRATEGIE.md interdit le développement produit avant le
  go de phase 2. La chaîne théorie→produit de cette session est un ARGUMENT (la théorie
  garantit la maintenabilité), pas un livrable. La discipline anti-dispersion ne bouge pas.

### Grandeurs mesurables ajoutées

- Fraction invariante par corpus et par domaine (technique, moral, quotidien).
- Accord inter-annotateurs synthétiques (juges multiples) — la barre de validité de I2.
- Taux de co-occurrence énoncés absolus ↔ moments de calibration (I3).
- Taux de couverture du fragment invariant pour la maintenance d'un graphe (I4).

### Questions ouvertes de la session 7

- Quels corpus d'explications humaines réelles ? (candidats : forums d'argumentation,
  avis motivés, textes d'instruction, transcriptions pédagogiques — à inventorier.)
- Les quantificateurs vagues (« souvent », « presque », « trop ») sont-ils dans le
  fragment ? (intuition : oui — ce sont des monotones ; à trancher dans I1.)
- **Le test multilingue** : si la langue parle en invariants pour des raisons de transfert
  entre bases, le fragment doit être grammaticalisé dans TOUTES les langues (comparatif,
  adpositions spatiales, marquage d'ordre temporel — la typologie semble dire oui).
  Prédiction forte, vérifiable sur corpus multilingues : l'universalité du fragment est
  un test de la conjecture que l'anglais seul ne peut pas fournir.

---

## Session 8 (2026-07-06) — Source et canal : la cognition fabrique les formes, la langue les transmet

### Énoncé brut (Reda)

> La cognition, c'est ces formes qui se construisent dans cet espace-là. La langue, c'est
> comment on les communique, comment on les envoie comme un signal. Et pour les tests
> industriels : je pense qu'on pourra générer des données selon nos besoins, contrôlées
> bien sûr — ce n'est pas un souci. On peut générer des données complètement conformes à
> des données générées par des humains, parce qu'on va bien contrôler les prompts et les
> tests.

### Formulation raffinée

1. **L'architecture source/canal.** Cognition = la SOURCE : la dynamique de formation des
   formes dans l'espace des qualités (les attracteurs de la session 6 vivent ici, côté
   source). Langue = le CODE DE CANAL : l'encodage des formes en signal transmissible.
   Pipeline complet : forme → encodage (fragment invariant) → canal entre bases
   désalignées → décodage → reconstruction de la forme chez le récepteur.
2. **Le corollaire de Shannon (deuxième pilier mathématique).** Les courbes
   d'explicabilité du repo — fidélité vs budget (feuilles, questions) — SONT des courbes
   débit-distorsion. Le désalignement réduit la capacité effective du canal : l'Exp 1 est
   une mesure de perte de capacité ; l'Exp 2 est un décodage interactif ; et **W_cal est
   le symbole pilote** — en télécommunications, on émet des pilotes connus pour estimer
   le canal ; la question de calibration (« et 12 000 €, c'est gros ? ») est exactement
   l'émission d'un pilote pour estimer la déformation monotone inconnue entre les deux
   bases. Les deux piliers se répondent : la théorie des groupes dit CE QUI passe le
   canal (les invariants), la théorie de l'information dit COMBIEN ça coûte.
3. **La distinction source/canal tranche A-G7 mieux que la version de la session 7.**
   Un LLM est entraîné sur le signal seul — jamais sur les formes. Il est donc un objet
   légitime pour toute affirmation sur le CODE (la langue, sa distribution, son fragment
   invariant), et illégitime pour toute affirmation sur la SOURCE (la cognition, la
   formation des formes). La conjecture est une affirmation sur le code → la génération
   synthétique est recevable, comme le soutient Reda. G2 (symbol grounding) est une
   affirmation sur la source → prudence maximale maintenue.
4. **La génération contrôlée, acceptée avec une échelle de validation.** Position de
   Reda entendue, reformulée en règle de méthode : la conformité aux données humaines
   n'est pas une propriété qu'on OBTIENT par l'artisanat du prompt — c'est une propriété
   qu'on MESURE. Protocole en strates :
   - **Strate 0** : corpus humain réel (petit, gratuit, existant) — l'ancre de validité.
   - **Strate 1** : juges synthétiques, validés par accord contre annotation humaine
     sur la strate 0.
   - **Strate 2** : génération synthétique contrôlée, validée distributionnellement
     contre la strate 0 AVANT toute extension d'échelle.
   - **Règle d'or** : tout résultat présent uniquement en strate 2 est un artefact de
     modèle jusqu'à preuve du contraire ; aucune affirmation du papier ne repose sur du
     purement synthétique.

### Attaques d'avocat du diable

- **A-G10 — Le prompt est une intervention.** « Bien contrôler les prompts » contient un
  paradoxe : chaque contrôle est une intervention sur la distribution qu'on prétend
  mesurer ; on ne peut pas à la fois contrôler et revendiquer la validité écologique.
  Résolution : le contrôle vit en strate 2, la validité vient de la strate 0 — le
  certificat de conformité est une distance distributionnelle mesurée, pas une promesse.
- **A-G11 — La dérive du tout-synthétique.** Le coût marginal quasi nul crée la tentation
  de ne plus jamais toucher de données humaines. Règle actée ci-dessus (strate 0
  obligatoire). Corollaire pratique : inventorier les corpus humains gratuits AVANT de
  générer quoi que ce soit (fait partie de I1/I2).

### Grandeurs mesurables ajoutées

- Distance distributionnelle strate 2 ↔ strate 0 : LE certificat de conformité de la
  génération (l'affirmation de Reda devient un nombre).
- Accord juges synthétiques ↔ annotation humaine sur strate 0 (validité de la strate 1).
- Les courbes fidélité/budget du repo relues en débit-distorsion — aucun nouveau calcul,
  une relecture.

### Questions ouvertes de la session 8

- La capacité du canal-langue est-elle formalisable ? (quelle mesure sur l'espace des
  formes ; lien candidat avec la taille de description à ε de la session 5.)
- Théorème des pilotes : combien de questions W_cal pour estimer une déformation monotone
  inconnue à δ près ? (la bissection de E1, session 3, donne O(log 1/δ) sur un axe —
  généralisation multi-axes à établir ; c'est la complexité d'estimation du canal.)
- La dynamique de la source (attracteurs, session 6) est-elle observable À TRAVERS le
  canal seul — ou faut-il un accès direct aux formes ? (si observable : la strate
  synthétique peut la détecter ; sinon, c'est une limite de principe des LLM.)
