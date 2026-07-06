# Pré-enregistrement F3 — campagne 1 (validation humaine de la grammaire I1 v0.2)

**Date de gel : 2026-07-06.** Ce document est écrit et commité AVANT tout
téléchargement ou ouverture des données de la campagne (discipline projet ;
A-G8, A-G18). Le commit git qui l'introduit fait foi d'horodatage.

**Références gelées** : `docs/GUIDE_ANNOTATION_F3.md` (guide GELÉ, commit
`5f2db04`) ; `docs/I1_grammaire_fragment_invariant.md` (grammaire I1 v0.2) ;
`experiments/pilote_f3/i1_classifier.py` (classifieur v2, correctif
fractions/dates inclus). Issue Linear : X-48. Pilote (orientation, ne prouve
pas — A-G23) : `docs/RESULTATS_PILOTE_F3.md`.

## 1. Objet et logique de la mesure

Le fait nécessaire **[F3]** du noyau (`noyau_geometrique_v0.1.md` §6) exige que
la grammaire I1 soit **opérationnalisable** : des juges humains indépendants
doivent classer les clauses réelles dans {A, I, C, N, OTHER} avec un accord
élevé. Si les clauses réelles sont majoritairement inclassables, [Déf 2.3]
n'est pas mesurable — F3 négatif, verrou de I2/I3.

Architecture de la mesure (deux étages, à ne pas confondre) :

1. **L'échantillon humain mesure l'accord (κ) et valide l'instrument**
   (précision/rappel du classifieur contre l'or humain adjudiqué). Il ne sert
   PAS à estimer les taux de classes — l'échantillon sur-représente
   délibérément la classe A (rare), toute estimation de taux y serait biaisée.
2. **Les taux corpus entiers (P1/P2a/P2b) restent mesurés par le classifieur**,
   qui n'est citable que si l'étage 1 le valide.

## 2. Hypothèses et critères de falsification (a priori)

- **H-κ (le verrou F3).** Accord inter-juges κ de Cohen ≥ **0,7** sur la
  classe A en binaire (A vs non-A), clauses en aveugle, 2 juges.
  κ global (5 classes exclusives) rapporté à titre descriptif, cible ≥ 0,6.
  **Falsification** : κ(A) < 0,7 ⇒ F3 négatif en l'état — la grammaire n'est
  pas opérationnalisable par des humains ; publication du résultat négatif,
  une seule révision du guide autorisée avant une campagne 2 (jamais
  d'amendement en cours de campagne).
- **H-V (validation de l'instrument).** Contre l'or humain adjudiqué :
  précision ET rappel du classifieur sur la classe A ≥ **0,8**.
  **Falsification** : rappel(A) < 0,8 ⇒ les taux P1 du pilote sont suspects
  (des A échappent à l'instrument) ; les chiffres corpus ne sont pas citables
  tant que l'instrument n'est pas corrigé et revalidé sur un NOUVEL
  échantillon.
- **H-R (ré-exécution locale).** La ré-exécution complète du pipeline v2
  (`run_pilote.py`, `run_recettes.py`) sur les corpus retéléchargés doit
  retrouver les chiffres du rapport §4/§9 : tolérance ±0,3 point sur chaque
  taux de classe, lift P2b dans [45, 75], ratio P2a dans [80, 130].
  **Falsification** : hors tolérance ⇒ divergence documentée, chiffres du
  rapport gelés comme non citables jusqu'à réconciliation.

Prédictions directionnelles maintenues (héritées du pilote, P1/P2a/P2b,
`RESULTATS_PILOTE_F3.md` §1) : elles sont déjà pré-enregistrées là-bas et ne
sont pas re-testées par l'échantillon humain de cette campagne (étage 2).

## 3. Échantillon (tirage AVANT annotation, seed gelée)

- **Taille : 300 clauses** (dans la fourchette 200–500 du guide §5).
- **Strates par registre** (origine masquée aux juges, ordre global mélangé) :
  - e-SNLI (explicatif) : 100 clauses ;
  - LIAR-PLUS (calibration) : 100 clauses ;
  - based.cooking (intermédiaire) : 50 lignes d'ingrédients + 50 phrases
    d'étapes.
- **Sur-échantillonnage de A** (pour que κ(A) soit estimable — A ~0,2 % en
  registre explicatif, un tirage uniforme n'en contiendrait aucun) : dans
  chaque strate, 30 % des unités sont tirées parmi les prédictions A du
  classifieur (ou la totalité s'il y en a moins), 70 % uniformément parmi le
  reste. Conséquence assumée : κ et précision/rappel seulement — pas de taux.
- **CoS-E exclu** de la campagne humaine (corpus notoirement bruité — décision
  a priori, pas après lecture des données).
- **Segmentation en clauses** : règle du guide §1 (découpe aux conjonctions et
  relatives), appliquée par un script déterministe ; les cas de segmentation
  douteux sont annotés tels quels (la clause affichée fait foi).
- **Seed unique du tirage : 20260706** (tirage déterministe, pas de
  re-tirage ; le multi-seed du protocole standard s'applique aux expériences
  stochastiques, pas à un échantillon d'annotation unique — décision
  documentée ici).

## 4. Procédure d'annotation

- **≥ 2 juges humains**, annotation **en aveugle** : feuilles sans étiquettes
  du classifieur, sans origine de corpus, ordre mélangé identique pour tous.
- Guide applicable : `GUIDE_ANNOTATION_F3.md` tel que gelé — tout cas limite
  nouveau est consigné, tranché en adjudication, versé au guide v-suivante,
  **jamais appliqué rétroactivement**.
- Multi-étiquettes autorisées (guide §1) ; la classe exclusive dérive de la
  priorité A > I > C > N > OTHER.
- **Adjudication** : désaccords tranchés à trois (les 2 juges + arbitre),
  consignés dans `experiments/f3/adjudication.md` ; l'or adjudiqué sert à H-V.

## 5. Mesures et résolution (A-G18)

Déclarées avant le jugement, jamais ajustées après :

- unité = la clause telle qu'affichée sur la feuille ;
- κ de Cohen par classe (binaire classe-vs-reste) + κ global sur la classe
  exclusive ; IC à 95 % par bootstrap (10 000 rééchantillonnages,
  seed 20260706) ;
- précision/rappel du classifieur par classe contre l'or adjudiqué, IC de
  Wilson à 95 % ;
- aucun retrait d'unité a posteriori (une clause illisible est annotée OTHER
  par consigne, pas supprimée).

## 6. Volet français — campagne 2 (pré-déclaré, non exécuté ici)

Aucun corpus français aligné (explicatif + calibration, public, gratuit) n'est
identifié à la date de gel. Le volet FR est une **campagne 2** distincte :
mêmes hypothèses H-κ/H-V, lexiques FR du guide §6 gelés, corpus proposés par
Reda (pilote §8). Rien du présent pré-enregistrement ne sera modifié
rétroactivement pour l'accueillir.

## 7. Données et coût

- Corpus (tous publics, gratuits, dépôts officiels) : e-SNLI (dev+test),
  CoS-E v1.11 (dev), LIAR-PLUS (val2+test2), based.cooking (markdown).
- **Aucun appel API payant** dans cette campagne (A-G8). Les juges sont
  humains ; aucun juge synthétique n'est utilisé avant que le go explicite de
  Reda et une validation contre l'or humain n'existent.

## 8. Livrables de la campagne

1. `resultats.json` régénéré (run v2) + verdict H-R.
2. `experiments/f3/` : échantillon (`sample_annotation.csv` pour les juges,
   `sample_key.csv` — prédictions classifieur + origine — tenu hors des yeux
   des juges), `kappa.py` (calcul κ/précision/rappel, IC).
3. Feuilles d'annotation remplies par les juges → verdicts H-κ puis H-V.
4. Mise à jour de `RESULTATS_PILOTE_F3.md` (statut ré-exécution) et de X-48.
