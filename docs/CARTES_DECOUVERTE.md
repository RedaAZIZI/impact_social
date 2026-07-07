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
