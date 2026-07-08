# Cartes de découverte — registre des pistes en réserve

**Ce qu'est ce registre.** Pendant les sessions, des idées « qui sentent la découverte »
apparaissent en marge du programme en cours. Les perdre serait un gâchis ; les poursuivre
immédiatement serait de la dispersion (A-G9). Ce registre les **gare** : chaque carte
spécifie l'idée assez précisément pour qu'une session future puisse la reprendre sans
réinventer, avec ses risques de collision et son critère de mort déjà posés.

**Discipline (non négociable) :**
- Une carte n'est PAS un engagement. Rien n'est codé, aucune expérience n'est lancée
  depuis une carte : elle doit d'abord être **promue** en session FONDAMENTAUX
  (énoncé brut → raffiné → attaques → mesurables) puis en document de programme.
- Chaque carte porte un **déclencheur d'activation** (quand a-t-on le droit d'y revenir)
  et un **critère de mort** (ce qui la tuerait) — écrits à la création, jamais adoucis.
- Statuts : `EN RÉSERVE` (garée) · `EN INSTRUCTION` (recherche externe ou interne en
  cours) · `PROMUE` (devenue session/doc — pointer lequel) · `TUÉE` (dire par quoi).
- Les collisions de littérature se vérifient AVANT toute survente (méthode REVUE_LITTERATURE).

**Gabarit** (toute nouvelle carte suit ces champs, dans cet ordre) :
ID · Titre · Date/Provenance · Statut · Énoncé brut · Formulation raffinée ·
Pourquoi ça sent la découverte (nouveauté candidate exacte) · Risques de collision ·
Prédictions falsifiables esquissées · Grandeurs mesurables · Critère de mort ·
Déclencheur d'activation · Dépendances.

---

## CD-1 — L'aspect linguistique comme taxonomie d'attracteurs

- **Date / provenance** : 2026-07-07, discussion de session (relecture PR #6, échange
  sur les formes dynamiques) ; intuition de Reda, bonus identifié en la raffinant.
- **Statut** : `EN RÉSERVE`.

### Énoncé brut (Reda, transcription)

> La représentation du langage dans l'espace de penser génère des formes dynamiques
> projetées sur l'univers de l'histoire (un temps latent intemporel émerge). Les formes
> sont des systèmes dynamiques avec deux ou trois attracteurs ; « un homme marche »
> est un système dynamique dans un espace latent ; une interaction est la relation
> entre deux séquences de cet environnement ; si sa vitesse est constante, la forme
> de la vitesse est statique (un point sur une ligne).

### Formulation raffinée

La linguistique classe les prédicats verbaux par **aspect** depuis Vendler (1957) :
états / activités / accomplissements / achèvements. Lecture en systèmes dynamiques
dans l'espace des qualités X (le cadre de [Déf 9.4] : trajectoires t ↦ x(t), formes
statiques = sections) :

| Classe de Vendler | Comportement qualitatif de trajectoire |
|---|---|
| État (« savoir », « être grand ») | point fixe — la trajectoire reste dans une région |
| Activité (« marcher », « pleuvoir ») | récurrence sans terme — cycle/attracteur, pas de frontière visée |
| Accomplissement (« traverser la rue ») | trajectoire transitoire AVEC franchissement d'une frontière de région nommée |
| Achèvement (« atteindre le sommet ») | l'événement de franchissement lui-même, ponctuel |

**Conjecture de la carte** : la taxonomie aspectuelle de la langue est la taxonomie
des comportements qualitatifs de trajectoires **invariants sous G_dyn = G ×
Reparam⁺(t)** (déformations monotones des axes ET du temps) — l'aspect est ce que la
langue peut dire d'une dynamique **sans horloge calibrée**. Indice interne fort : le
test linguistique classique des aspects (« pendant une heure » vs « en une heure »)
recoupe la *subinterval property* (Bennett & Partee) — les états/activités sont
invariants par restriction temporelle, les accomplissements non. Un critère
d'invariance est donc DÉJÀ le test opératoire des linguistes, sans qu'ils le
formulent en théorie des groupes.

### Pourquoi ça sent la découverte (nouveauté candidate exacte)

Pas « classifier l'aspect » (fait depuis 1957), pas « aspect et structure
d'événements » (Dowty, Moens & Steedman, Croft — semi-formel). La nouveauté candidate :
**dériver** la taxonomie aspectuelle comme classification des invariants de
trajectoires sous reparamétrisation monotone du temps — lecture Erlangen de l'aspect,
symétrique de ce que T2 fait pour les comparatifs. Corollaire attendu : les durées
chiffrées (A temporels) se greffent sur les prédicats téliques (le franchissement se
calibre : « en 10 minutes »), pas sur les activités pures — même mécanique que W_cal.

### Risques de collision (à vérifier AVANT toute rédaction)

Vendler 1957 ; Dowty 1979 (aspect calculus) ; Bennett & Partee (subinterval property) ;
Moens & Steedman 1988 (temporal ontology) ; Galton 1984 (*The Logic of Aspect*) ;
Krifka (télicité, méréologie) ; **Croft 2012** (*Verbs: Aspect and Causal Structure* —
représentations géométriques 2D de l'aspect : le risque le plus direct) ; Talmy
(force dynamics) ; Steedman (*The Productions of Time*) ; physique qualitative
(Kuipers, Forbus) côté trajectoires qualitatives.

### Prédictions falsifiables esquissées

1. Le classement des prédicats par juges (tests aspectuels standard) coïncide avec le
   classement par type de comportement qualitatif de trajectoires simulées/annotées.
2. La distribution des classes de Vendler varie par registre comme la densité de
   franchissements le prédit (procédural ≫ narratif ≫ explicatif en accomplissements).
3. Co-occurrence : A-temporels (durées chiffrées) concentrés sur les prédicats
   téliques ; quasi absents des activités — mesurable avec l'instrument F3 étendu.

### Grandeurs mesurables

κ inter-juges sur la classe aspectuelle ; taux de classes de Vendler par registre ;
lift de co-occurrence A-temporel × télicité (même forme que le lift P2b du pilote).

### Critère de mort

(1) Croft/Galton/Dowty contiennent déjà la dérivation invariance-théorique complète
(pas seulement une géométrie descriptive) ; (2) les classes de Vendler ne sont pas
stables inter-juges sur corpus réel ; (3) la correspondance ne survit pas hors de
l'anglais.

### Déclencheur d'activation

Après (a) la campagne F3 n° 1 rendue (l'instrument d'annotation doit exister avant de
l'étendre à l'aspect) ET (b) le retour de l'instruction externe CD-2 (le théorème des
invariants temporels est le socle formel de cette carte).

### Dépendances

`noyau_geometrique_v0.1.md` [Déf 9.4], A-G17 (toute affirmation dynamique se projette
sur une section statique mesurable ; vocabulaire : récurrence/cycle/attracteur —
jamais « onde/vibration » en public) ; grammaire I1 v0.2 (l'extension aspectuelle ne
touche pas le guide F3 gelé, A-G18) ; carte CD-2.

---

## CD-2 — L'invariant maximal sous reparamétrisation monotone du temps (le temps latent ordinal)

- **Date / provenance** : 2026-07-07, même discussion — la description de Reda :
  les formes dynamiques projetées sur l'univers de l'histoire font émerger un
  **temps latent** sans métrique (« intemporel ») ; candidat théorème T4, symétrique
  temporel de T2.
- **Statut** : `EN INSTRUCTION` (recherche théorique externe lancée le 2026-07-07,
  prompt archivé dans cette discussion ; le résultat sera rapporté en session pour
  relecture adverse avant toute intégration aux preuves).

### Énoncé de la question instruite

Caractériser l'invariant maximal d'une trajectoire (et d'un couple de trajectoires)
dans un produit d'axes ordonnés, sous G_dyn = déformations monotones par axe ×
reparamétrisations monotones du temps. Conjecture : l'invariant maximal est la donnée
ordinale — ordre des événements (franchissements, croisements, extrema), relations
d'ordre inter-axes, suite symbolique par partition compatible — durées et vitesses
détruites (→ A temporels, W_cal).

### Ce qui en dépend

Le socle formel de CD-1 ; l'éventuelle extension narrative de la conjecture des
invariants (la langue du récit) ; la lecture « monitoring qualitatif explicable »
côté produit. Intégration aux preuves (T4) UNIQUEMENT après relecture adverse
(discipline preuves v0.2/v0.3).

---

## CD-3 — Annotation par décomposition binaire (le pont vers l'annotation industrielle)

- **Date / provenance** : 2026-07-07, discussion en préparation de l'annotation F3 ;
  intuition de Reda, consignée sur sa validation.
- **Statut** : `EN RÉSERVE`.

### Énoncé brut (Reda, transcription)

> Faire un truc semi-industriel, où chaque mot on coche plusieurs cases binaires de
> ce qu'il est et ce qu'il n'est pas, vis-à-vis de certaines formes dans certains
> espaces.

### Formulation raffinée

Remplacer le jugement holistique de classe (une étiquette parmi {A,I,C,N,OTHER})
par une **liste de contrôle de tests binaires explicites**, cochés séparément par
unité, la classe étant DÉRIVÉE mécaniquement des cases. L'arbre de décision du guide
(§3) est déjà cette suite de tests (« contient un numéral ? », « suivi d'une
unité ? », « marqueur relationnel ? », « graduable en forme positive ? ») — la carte
propose de l'exposer comme interface d'annotation au lieu de le faire composer de
tête. Lecture théorique : une case binaire = un test d'appartenance à une région
nommée dans un espace de traits — l'annotation devient l'évaluation de prédicats de
formes, cohérente avec le noyau.

### Pourquoi ça sent la découverte (au sens : gain méthodologique structurant)

1. **Fiabilité** : les questions binaires simples donnent un accord inter-juges
   supérieur au choix multi-classes (résultat standard en annotation de corpus) —
   κ devrait monter.
2. **Désaccord diagnostiquable** : on voit QUELLE case diverge entre juges ;
   l'adjudication devient quasi mécanique et nourrit le guide case par case.
3. **Interface exacte du pipeline industriel** : chaque case est automatisable et
   validable SÉPARÉMENT contre l'or humain — le partage humain/machine (humains sur
   les cases dures, machine sur les cases faciles) tombe naturellement ; c'est le
   chaînon entre F3 (artisanal) et I2 (annotation synthétique industrielle,
   session 7 « force humaine synthétique »).

### Question ouverte attachée (À DISCUTER — décision de Reda requise)

Remplacer « 2 juges humains » par « 1 humain + plusieurs modèles différents » dans
les campagnes futures. Termes du débat consignés : le pré-enregistrement campagne 1
l'interdit (juges synthétiques seulement après go explicite + validation contre or
humain — circularité : l'or humain vient d'abord) ; [F3] mesure l'opérationnalisable
PAR DES HUMAINS ; erreurs corrélées entre modèles et avec les lexiques du
classifieur (κ gonflé) — la diversité des modèles atténue-t-elle assez la
corrélation ? Chaîne sanctionnée : or adjudiqué campagne 1 → validation des juges
modèles (précision/rappel type H-V) → bras synthétiques multiples + 1 humain
d'ancrage. Coût API : go de Reda palier par palier (A-G8).

### Risques de collision

Littérature de méthodologie d'annotation (decomposed/checklist annotation,
Pustejovsky & Stubbs ; travaux LLM-as-annotator et accords humain-modèle) — à
balayer avant d'en revendiquer quoi que ce soit ; ici le statut visé est un GAIN
D'INGÉNIERIE du protocole, pas une contribution théorique.

### Prédictions falsifiables esquissées

1. κ(A) en mode checklist ≥ κ(A) en mode holistique sur un même sous-échantillon.
2. La classe dérivée des cases reproduit la classe exclusive du guide (priorité
   A>I>C>N>OTHER) dans ≥ 95 % des cas — sinon l'arbre du guide est ambigu et la
   divergence localise l'ambiguïté.
3. Les cases « faciles » (numéral présent, symbole monétaire) atteignent un accord
   quasi parfait et sont automatisables sans perte ; le désaccord résiduel se
   concentre sur 2-3 cases identifiables (graduables, composés lexicalisés).

### Grandeurs mesurables

κ par CASE (pas seulement par classe) ; taux de reproduction de la classe dérivée ;
répartition du désaccord par case ; coût d'annotation par clause (temps) dans les
deux modes.

### Critère de mort

Le mode checklist ne fait PAS monter κ(A) (ou le fait baisser — sur-fragmentation,
fatigue) ; ou la classe dérivée diverge structurellement du jugement holistique
(l'arbre du guide ne capture pas ce que les juges font réellement — ce qui serait
en soi un résultat sur la grammaire).

### Déclencheur d'activation

La CONCEPTION de la campagne 2 (volet FR, pré-déclaré) ou du pipeline I2 — jamais la
campagne 1 en cours (guide et procédure gelés, A-G18). La question ouverte
« 1 humain + N modèles » se tranche en session dédiée avec Reda, après le verdict
H-κ de la campagne 1.

### Dépendances

`GUIDE_ANNOTATION_F3.md` §3 (l'arbre, matière première des cases) ;
`PREREGISTREMENT_F3.md` §6-§7 (campagne 2, interdit synthétique) ; programme I2
(STRATEGIE, session 7) ; or adjudiqué de la campagne 1 (préalable à toute
validation de juges modèles).
