# Bilan du projet REX — préparation de la pose du drapeau

**But** : inventorier tout ce qui est acquis, proposer le récit et la structure du preprint
arXiv (le drapeau, phase 1 de STRATEGIE.md), et lister les décisions qui reviennent à Reda.
Périmètre assumé : **pas** de « très grand graphe apprenant en temps réel » — le programme
REX-LLM reste en pause de recul ; le drapeau se plante sur ce qui est démontré.

---

## 1. Les acquis, en chiffres

### Corpus v0 — monde synthétique, vérité terrain explicative connue (article source, sections 5-9)

| Exp | Résultat | Chiffres clés |
|---|---|---|
| 1 | Le coût d'explicabilité croît de façon monotone avec le désalignement des bases | AUC 0.918 (θ=0) → 0.745 (θ=1.5) ; budget pour 95 % : 16 feuilles vs jamais (>256) dès θ≥0.4 ; 10 seeds |
| 1b | Invariance aux déformations monotones ; le coût = le mélange des dimensions | AUC identique linéaire vs tanh (0.7432/0.7433/0.7433) |
| 2 | L'explication est un protocole mesurable (nombre de questions W) | 6 questions → 92 % aligné (97.9 % à 15) ; plafond ~71 % désaligné, mêmes réponses de M |
| 3 | Le canal est bidirectionnel : 1 phrase d'édition > 3000 exemples de fine-tuning | 0.990 ± 0.004 vs 0.968 ± 0.004 ; sans adaptation 0.741 |
| 4 | L'explicabilité dépend de la question Q, asymétriquement | taille contrastive 2.95 → 6.39 selon Q |

### Corpus nouveau — données réelles et régime interactif (cette itération)

| Exp | Résultat | Chiffres clés |
|---|---|---|
| 5 (German Credit, réel) | **Infirmation propre** : pas de dominance du vocabulaire expert — le monde du crédit n'est pas écrit en concepts composés | écart −0.003 ± 0.019 (2 runs, critère pré-enregistré) ; leçon de méthode : normaliser par la fidélité du modèle trivial |
| 6 (AI4I 2020, réel) | **Première démonstration du désalignement naturel sur données réelles** (terrain physique) ; l'écart dépend de la base interne de M | MLP : +0.045 ± 0.010 (>4σ) ; GBT (axis-aligned par construction) : +0.004 ± 0.023 — la thèse relationnelle observée côté modèle |
| 7 (le graphe qui vit, pré-enregistré) | **15 phrases (0 étiquette) battent 75 000 étiquettes de réentraînement** sur 15 dérives ; zéro dégradation cumulative | graphe 0.990 ± 0.003 vs réentraîné 0.981 ± 0.002 vs fine-tuné 0.854 ± 0.018 vs figé 0.624 ; intégrité région jamais éditée 0.992 → 0.994 ; phrases bruitées ±0.10 : 0.971 ; désaligné θ=1.5 : 0.801 (taxe ~0.19) ; 4 conditions de mort pré-enregistrées, toutes survécues |
| Prop 1 (invariance monotone) | Confirmée sur **tous** les bancs d'essai, synthétiques et réels — 7 runs sur 7, souvent exactement 0.0000 | quasi-théorème : preuve à rédiger (les arbres à seuils ne dépendent que des ordres) |

### Infrastructure (conditions du drapeau)

- Repo structuré : `/experiments` (7 scripts reproductibles, seeds fixées), `/core` (librairie
  `rex` : RuleListModel, W, W⁻¹, métriques), `/tests` (10 tests verts dont **l'invariant de
  localité de l'édition**), `/figures`, `/docs`, LICENSE Apache-2, CITATION.cff.
- Reproductibilité vérifiée : exp1b_exp4 relancée de zéro → chiffres identiques à l'article.
- Discipline établie et démontrée : hypothèses a priori, critères de falsification,
  pré-enregistrement horodaté (Exp 7, Exp 8), infirmations publiées (Exp 5).
- Fondamentaux en cours de clarification (sessions 1-3 : boucle rétroactive et politiques,
  superposition de graphes, opérateur W_cal) — **matière à perspectives, pas à sections**.

## 2. Le récit du preprint (proposition)

Le papier initialement prévu disait : « voici un cadre, et des preuves de concept
synthétiques ». On peut maintenant dire beaucoup mieux, sans rien survendre :

1. **Thèse** : l'explicabilité est une propriété de la relation (M, R, Q), pas du modèle ;
   la XAI classique est le cas dégénéré base(M) = base(R).
2. **Preuves synthétiques contrôlées** (Exp 1-4) : monotonie au désalignement, protocole W,
   canal bidirectionnel, dépendance à Q.
3. **Le cadre survit au contact du réel — dans les deux sens** (le diptyque) : pas de
   dominance là où le monde n'est pas écrit en concepts composés (German Credit, infirmation
   propre) ; dominance nette là où il l'est (maintenance prédictive AI4I). Le désalignement
   naturel existe et on sait prédire où.
4. **La relation a deux côtés** : à monde et récepteurs fixés, l'écart dépend de la base
   interne de M (GBT axis-aligned : nul ; MLP : net) — même la question « pour qui M
   est-il explicable ? » dépend de *quel* M.
5. **Le régime interactif** (Exp 3 + Exp 7) : le canal sémantique bat le gradient en régime
   de dérive — 15 phrases > 75 000 étiquettes, zéro oubli par construction, robuste à
   l'imprécision humaine, taxé (mesurablement) par le désalignement. Formulé en conjecture
   assumée : « paradigme candidat post-gradient ».
6. **Limites explicites** : basse dimension, mondes compressibles, phrases d'oracle
   localisées (A1 ouvert), pas de validation humaine, pas d'échelle LLM.
7. **Perspectives (une ligne chacune)** : validation humaine ; algorithme A1 ; compression
   contextuelle de LLM ; base commune construite par boucle rétroactive, superposition de
   graphes et opérateur de calibration (fondamentaux en cours).

**Figures proposées (4)** : exp1_courbes (la thèse), exp2_dialogue (le protocole),
exp6_ai4i (le réel), exp7_living_graph (le régime interactif). Les tableaux portent le reste.

## 3. Claims autorisés / interdits (sobriété, section 13 de l'article source)

**Autorisés** : tout ce qui est dans les tableaux ci-dessus, avec les barres d'erreur ;
« première mesure du désalignement naturel sur données réelles » (à conditionner à la
vérification biblio) ; « pré-enregistré, conditions de mort publiques » (git fait foi).
**Interdits** : toute généralisation aux humains ; « fonctionne à l'échelle » ; « remplace
le gradient » (c'est une conjecture, dire conjecture) ; tout chiffre sans tableau source.

## 4. Ce qui reste avant soumission (mécanique)

1. Intégrer les Exp 5-7 dans `docs/article_source_explicabilite.md` (sections nouvelles,
   même format que 5-9 : protocole, tableau, interprétation, et l'infirmation de l'Exp 5
   traitée avec les mêmes honneurs que les confirmations).
2. Conversion LaTeX arXiv 6-8 pages (S-57), biblio vérifiée + ajouts nécessaires
   (S-58 ; ajouter : common ground si les fondamentaux entrent en perspective).
3. Reproduction de zéro d'exp1_solid / exp2 / exp3 pour verrouiller chaque chiffre cité
   (S-54 — exp1b déjà validée).
4. Relecture par Reda du README et des formulations de claims (S-56).

## 5. Décisions qui reviennent à Reda (bloquantes pour le drapeau)

| # | Décision | Options |
|---|---|---|
| D1 | **Titre** | Les 3 propositions de la section 1 de l'article source ; ma préférence : *« Explainability is Relational: A Receiver-Dependent Framework for AI Interpretability »* |
| D2 | **Périmètre du preprint** | (a) v0 synthétique seul (fidèle au plan initial) ; (b) v0 + Exp 5-7 (recommandé : le diptyque réel et le pré-enregistrement changent la crédibilité du papier) |
| D3 | **Repo public** | **TRANCHÉ (2026-07-06)** : le repo reste `impact_social` — pas de nouveau repo. Reste : merger la PR #1 et passer le repo en public au moment de la soumission |
| D4 | **Auteur / affiliation** | nom exact, affiliation, ORCID éventuel pour arXiv |
| D5 | **Endorsement arXiv** | cs.LG demande parfois un endorsement pour un premier dépôt — vérifier ton statut, sinon prévoir la demande |

**Ce qu'on ne fait pas pour le drapeau** (discipline) : pas de gros graphe temps réel,
pas d'appels LLM, pas de nouvelles expériences — le corpus actuel suffit et le recul
sur les fondamentaux continue en parallèle sans bloquer la soumission.
