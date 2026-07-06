# L'explicabilité comme propriété relationnelle : un cadre récepteur-dépendant pour l'interprétabilité de l'IA

**Document source pour rédaction d'article scientifique — vision, formalisation, protocoles et résultats expérimentaux complets.**
*Format cible : position paper avec résultats préliminaires (workshop NeurIPS/ICML, ou preprint arXiv). Auteur de la vision et de l'approche : Reda. Expériences : prototypes reproductibles inclus.*

---

## 1. Titre (propositions)

1. *Explainability is Relational: A Receiver-Dependent Framework for AI Interpretability*
2. *Why-Operators and Receiver Bases: Rethinking Explainability as an Interactive Protocol*
3. *There Is No Explainability Without a Receiver: Evidence from Basis-Misalignment Experiments*

## 2. Abstract (brouillon)

L'explicabilité en IA est traitée comme une propriété intrinsèque du modèle. Nous soutenons que c'est une erreur de catégorie : l'explicabilité est une propriété de la **relation** entre un modèle M et un récepteur R, chacun doté de sa propre base représentationnelle. Nous montrons que la XAI classique (attributions de features, arbres de substitution) est le cas dégénéré où les bases de M et R sont supposées identiques. Nous proposons (i) une définition formelle : M est explicable pour R ssi il existe un graphe de décision, exprimé dans le vocabulaire de prédicats de R et de complexité bornée, qui simule M à fidélité ε ; (ii) un **opérateur pourquoi** W, contrastif et composable, faisant de l'explication un protocole interactif dont le coût (nombre de questions) mesure l'explicabilité ; (iii) deux expériences contrôlées sur monde synthétique où la vérité terrain explicative est connue. Résultats : le coût d'explicabilité croît de façon monotone et continue avec l'angle de désalignement des bases (AUC de fidélité : 0.918 → 0.745) ; la reconstruction du graphe de M par questions successives converge en ~6 questions en base alignée (fidélité 97.9%) et ne converge pas en base désalignée (plafond 71%). Même modèle, mêmes explications : seule la base du récepteur change. Nous esquissons les implications : compression contextuelle de grands modèles en graphes explicables, et apprentissage par édition de graphe en dialogue.

## 3. La vision (section introduction / motivation)

### 3.1 Le problème caché de la XAI
Entre humains, l'explication fonctionne parce qu'une base commune (langage, concepts, culture) est partagée par défaut — un canal jamais formalisé parce que jamais défaillant. Avec l'IA, cette hypothèse tombe : les features internes d'un réseau ne coïncident pas avec les concepts humains. Or toutes les méthodes classiques (SHAP, LIME, saliency maps, arbres de substitution) supposent implicitement que les axes du modèle SONT les concepts du récepteur. Elles calculent une explication dans la base de M et la livrent telle quelle à R.

### 3.2 La thèse
**L'explicabilité n'est pas une propriété de M. C'est une propriété du triplet (M, R, Q)** : le modèle, la base du récepteur, et la question contextuelle posée. La XAI classique = le cas particulier base(M) = base(R) et Q = « pourquoi cette sortie ? » sans contraste explicite.

### 3.3 La vision long terme (section discussion / perspectives)
Si l'explication est un protocole interactif (série de « pourquoi ? »), le même canal sert à apprendre : l'opérateur inverse de W insère des fragments de graphe fournis par R dans M. Perspectives : (a) IA apprenant en dialogue par édition de graphe — locale, instantanée, traçable — plutôt que par descente de gradient ; (b) compression contextuelle : un grand modèle (milliards de paramètres) distillé à la volée, selon le contexte, en un graphe de ~10⁶ paramètres, spécialisé, exécutable localement, entièrement explicable ; (c) IA personnelle qui grandit avec son utilisateur. Trade-off performance/interprétabilité reconnu, mais évalué sur benchmarks statiques : en régime interactif, un graphe corrigeable en une phrase peut battre un réseau figé exigeant un réentraînement. Thèse falsifiable, non testée dans la littérature.

**Les deux forces structurelles du paradigme (à mettre en avant).** L'apprentissage par édition de graphe attaque frontalement les deux faiblesses les plus documentées du deep learning : (i) l'**inefficacité en données** — une phrase sémantique compresse ce que des milliers d'exemples expriment (Exp 3 : 1 phrase > 3000 exemples) ; (ii) l'**oubli catastrophique** — l'édition étant locale, la correction d'une règle ne peut mécaniquement pas dégrader les autres régions. Ce n'est pas une atténuation du problème : c'est son inexistence par construction. Formulation à employer (conjecture assumée, pas claim établi) : « Nous conjecturons que l'apprentissage par édition de graphe en dialogue constitue un paradigme candidat pour l'apprentissage post-gradient : efficace en données parce que le canal est sémantique, et continual par construction parce que l'édition est locale. »

## 4. Cadre formel (section méthode / théorie)

### 4.1 Définitions
- **Récepteur** R = (V_R, C_R) : un vocabulaire de prédicats V_R (les tests que R sait évaluer/comprendre) et une contrainte de capacité C_R (taille max de structure).
- **Explication candidate** : un graphe de décision G dont chaque nœud est un prédicat de V_R, les arêtes le flux conditionnel, les feuilles les sorties.
- **Explicabilité** : Expl(M, R, ε) = min { |G| : G exprimé dans V_R, fidélité(G, M) ≥ 1−ε }, avec fidélité = accord sur la distribution de données. M est explicable pour R au niveau (ε, K) ssi Expl(M, R, ε) ≤ K.
- **Courbe d'explicabilité** : fidélité maximale atteignable en fonction du budget |G| — la signature d'explicabilité de M relative à R. Métrique scalaire associée : AUC de la courbe.
- **Cas dégénéré (théorème informel à rédiger)** : si V_R = prédicats à seuil sur les features d'entrée de M (base identité), on retrouve la distillation en arbre classique ; la XAI standard est l'explicabilité généralisée restreinte à l'alignement parfait.

### 4.2 Deux axes de complexité
Complexité structurelle (taille du graphe) × complexité des prédicats (le vocabulaire V_R). Un graphe petit à prédicats denses (w·x > θ) n'est pas lisible ; un graphe axis-aligned l'est. La « base du récepteur » = V_R.

### 4.3 La question contextuelle Q (théorie pragmatique)
Ancrage : van Fraassen — toute question « pourquoi ? » est contrastive (« pourquoi A plutôt que B ? ») et le contexte sélectionne le contraste. Dans notre cadre : la réponse à Q = le sous-graphe minimal où les chemins vers A et vers B divergent (les nœuds pivotaux). Les explications contrefactuelles de la XAI sont un cas particulier. L'explicabilité complète devient une moyenne (ou pire cas) sur la distribution des Q du contexte d'usage.

### 4.4 L'opérateur W (pourquoi)
W(x, contraste) → sous-graphe minimal pivotal, exprimé dans V_R. Trois propriétés exigées : **minimalité** (aucun nœud superflu), **traduisibilité** (sortie dans le vocabulaire de R), **composabilité** (les réponses s'assemblent). L'explication devient un protocole : R pose des W successifs jusqu'à simulatability suffisante — le « ah d'accord » formalisé. **Nouvelle mesure d'explicabilité : le nombre de questions W nécessaires pour reconstruire M à fidélité ε.** Lien théorique : exact learning d'Angluin (requêtes d'appartenance/équivalence — W est une requête plus riche) ; lien avec preuves interactives et debate (récepteur = vérifieur borné) à mentionner en perspective seulement.

### 4.5 Littérature à citer (ancres)
- Alignement représentationnel : CKA (Kornblith et al.), Procrustes, model stitching.
- Simulatability comme métrique d'explication (Doshi-Velez & Kim ; Hase & Bansal).
- Théorie pragmatique de l'explication : van Fraassen, *The Scientific Image* (1980).
- Explications contrastives/contrefactuelles : Miller (2019), Wachter et al.
- Distillation en arbres : Frosst & Hinton (soft decision trees) ; TREPAN (Craven & Shavlik).
- Exact learning : Angluin (1988).
- Trade-off interprétabilité/performance : Rudin (2019) — à discuter et nuancer.
- Un réseau ReLU est exactement un graphe de décision exponentiel → la question devient la compressibilité (analogie Kolmogorov restreinte aux graphes).
- Oubli catastrophique : McCloskey & Cohen (1989) ; French (1999) ; Kirkpatrick et al. (EWC, 2017) — le problème que l'édition locale supprime par construction.
- Model editing dans les LLM : ROME (Meng et al., 2022), MEMIT (Meng et al., 2023) — à citer et s'en différencier : ils éditent des poids opaques via des heuristiques de localisation fragiles ; ici on édite une structure explicable via le canal même de l'explication (l'édition est un sous-produit du cadre, pas une technique ad hoc).
- Machine teaching : Zhu (2015) — efficacité en données du canal sémantique/enseignant.
- Datasets réels : Statlog German Credit (Hofmann, UCI n°144) ; AI4I 2020 Predictive Maintenance (Matzka, 2020, UCI n°601) — années et références exactes à vérifier.

## 5. Expérience 1 — L'explicabilité est relative à la base du récepteur

### 5.1 Protocole
- **Monde synthétique** : 6000 objets, 5 attributs interprétables ~ U[0,1] : taille, teinte, forme, position x, position y.
- **Graphe vrai G\*** (écrit à la main, vérité terrain explicative) :
  - SI taille > 0.6 ET teinte > 0.5 → classe A
  - SINON SI forme > 0.7 → classe B
  - SINON SI pos_x < 0.3 ET pos_y < 0.3 → classe A
  - SINON SI teinte < 0.2 ET taille < 0.4 → classe B
  - SINON → classe C
- **Modèle opaque M** : MLP 2×50 neurones, entraîné sur (X, G\*(X)). Accuracy : 0.9762 ± 0.0059 (10 seeds).
- **Manipulation** : récepteurs définis par leur base = rotation de force θ appliquée aux 5 dimensions (matrice antisymétrique aléatoire normalisée A, R = expm(θA) ; θ=0 → identité). θ ∈ {0, 0.2, 0.4, 0.8, 1.5}.
- **Mesure** : distillation de M en arbre (prédicats à seuil dans la base du récepteur), budget ∈ {2,...,256} feuilles ; fidélité = accord arbre/MLP sur test. 10 seeds, moyenne ± écart-type.

### 5.2 Résultats (tableau complet)

| Budget | θ=0.0 | θ=0.2 | θ=0.4 | θ=0.8 | θ=1.5 |
|---|---|---|---|---|---|
| 2 | 0.696±0.015 | 0.678±0.013 | 0.654±0.014 | 0.595±0.030 | 0.549±0.041 |
| 4 | 0.834±0.011 | 0.794±0.026 | 0.737±0.035 | 0.678±0.030 | 0.641±0.035 |
| 8 | 0.936±0.009 | 0.895±0.014 | 0.835±0.014 | 0.736±0.017 | 0.705±0.023 |
| 16 | 0.976±0.007 | 0.934±0.012 | 0.879±0.014 | 0.791±0.018 | 0.752±0.020 |
| 32 | 0.977±0.007 | 0.944±0.010 | 0.904±0.015 | 0.829±0.018 | 0.795±0.016 |
| 64 | 0.975±0.008 | 0.949±0.007 | 0.917±0.013 | 0.852±0.014 | 0.824±0.019 |
| 128 | 0.975±0.008 | 0.952±0.008 | 0.920±0.012 | 0.872±0.014 | 0.841±0.017 |
| 256 | 0.975±0.008 | 0.950±0.008 | 0.921±0.010 | 0.878±0.013 | 0.855±0.014 |

- **AUC d'explicabilité** (fidélité moyenne sur budgets) : θ=0 : **0.918** ; θ=0.2 : 0.887 ; θ=0.4 : 0.846 ; θ=0.8 : 0.779 ; θ=1.5 : **0.745**. Monotonie stricte.
- **Budget minimal pour fidélité ≥ 0.95** : θ=0 : **16 feuilles** ; θ=0.2 : 128 ; θ≥0.4 : **jamais atteint (>256)**.
- Figure : `exp1_courbes.png` (courbes fidélité/budget par θ, bandes ± std).

### 5.3 Interprétation
Même modèle M (pas un poids ne change), même information (rotations = bijections). Seule la base du récepteur varie → les courbes d'explicabilité divergent de façon monotone avec θ. L'explicabilité n'est donc pas une propriété de M. Le critère de falsification était défini a priori (courbes superposées = concept vide) ; il est passé.

## 6. Expérience 2 — L'opérateur W et la reconstruction par pourquoi successifs

### 6.1 Protocole
- Même monde, même M. Graphe de référence de M : arbre 32 feuilles distillé en base originale (proxy du « graphe de M »).
- **Opérateur W(x)** : « pourquoi x est classé c ? » → la règle = chemin de décision de x (conjonction de prédicats (feature, seuil, direction)) + classe. Implémente minimalité (chemin) et contraste implicite (vs autres feuilles).
- **Protocole de dialogue (apprentissage actif)** : le récepteur part d'un prédicteur trivial (classe majoritaire) ; à chaque tour, il choisit un point où il est en désaccord avec M, pose W, intègre la règle, recommence. 15 questions max, 5 seeds.
- **R-aligné** : stocke la règle exacte (même vocabulaire). Prédiction : première règle qui matche, sinon défaut.
- **R-pivoté (θ=1.5)** : ne perçoit le monde que dans sa base tournée ; chaque règle reçue (région axis-aligned dans la base de M = polytope oblique dans la sienne) doit être approximée par un petit arbre (8 feuilles) dans SON vocabulaire.
- **Mesure** : fidélité à M du modèle reconstruit, en fonction du nombre de questions.

### 6.2 Résultats

| Questions | R-aligné | R-pivoté (θ=1.5) |
|---|---|---|
| 0 | 0.457±0.010 | 0.457±0.010 |
| 3 | 0.727±0.089 | 0.625±0.046 |
| 6 | **0.921±0.022** | 0.688±0.024 |
| 9 | 0.966±0.002 | 0.695±0.021 |
| 12 | 0.977±0.006 | 0.703±0.027 |
| 15 | **0.979±0.007** | **0.713±0.024** |

- **Questions pour atteindre 90% de fidélité : R-aligné = 6 ; R-pivoté = jamais (15 questions).**
- Remarque structurelle : G\* a ~7 branches ; ~6 questions suffisent — le dialogue reconstruit la structure à raison d'environ une règle par question.
- Figure : `exp2_dialogue.png`.

### 6.3 Interprétation
L'explicabilité-comme-protocole est mesurable : le nombre de pourquoi est petit et fini quand les bases sont alignées ; le dialogue ne converge pas quand elles sont désalignées — **avec les mêmes réponses de M**. Deux protocoles indépendants (distillation statique, dialogue interactif) confirment la même thèse.

## 7. Expérience 3 — L'opérateur inverse : apprendre par le dialogue

### 7.1 Protocole (scénario concept drift)
- Le monde change : la règle « forme > 0.7 → B » de G\* devient « forme > 0.7 → A ». M, entraîné sur l'ancien monde, tombe à 0.741 d'accuracy sur le nouveau.
- **Voie A (notre cadre)** : le graphe explicable de M (liste de règles extraite de l'arbre de référence 32 feuilles) est corrigé par UNE phrase de dialogue — « quand forme > 0.7, c'est A maintenant » — implémentée comme édition de la classe des règles concernées (opérateur inverse de W). Coût : 1 interaction, 0 gradient.
- **Voie B (paradigme standard)** : le MLP est fine-tuné (warm start, 50 époques) sur n ∈ {10,...,3000} nouveaux exemples étiquetés.
- Accuracy mesurée sur le nouveau monde, 5 seeds.

### 7.2 Résultats
| Méthode | Coût | Accuracy nouveau monde |
|---|---|---|
| M sans adaptation | — | 0.741 ± 0.012 |
| **Édition de graphe (dialogue)** | **1 phrase** | **0.990 ± 0.004** |
| Fine-tuning | 10 exemples | 0.758 ± 0.046 |
| Fine-tuning | 100 exemples | 0.893 ± 0.012 |
| Fine-tuning | 1000 exemples | 0.947 ± 0.004 |
| Fine-tuning | 3000 exemples | 0.968 ± 0.004 |

**Une phrase de dialogue surpasse 3000 exemples de fine-tuning** (0.990 vs 0.968). L'édition est instantanée, locale (les régions non concernées sont intactes par construction — pas d'oubli catastrophique possible), et traçable. Figure : `exp3_dialogue_vs_finetuning.png`.

### 7.3 Interprétation et fair-play méthodologique
La comparaison n'est pas « à information égale » : une phrase sémantique compresse l'équivalent de milliers d'exemples — c'est précisément la thèse. Le canal d'explication (W) et le canal d'apprentissage (W⁻¹) sont le même canal, utilisé dans les deux sens. Ceci opérationnalise la vision : une IA qui apprend au moment où on lui parle, par édition de graphe plutôt que par descente de gradient. À noter : la voie A exige que la correction soit exprimable dans le vocabulaire partagé — en base désalignée (Exp 1-2), ce canal se dégrade, ce qui relie les trois expériences en un seul récit.

## 8. Expérience 1b — Le désalignement non linéaire (résultat de structure)

Protocole : base du récepteur v = tanh(s·(x−0.5)·R) avec R la rotation θ=1.5 et s la force de la non-linéarité (s∈{2,6}), 5 seeds. Résultat : AUC identique au cas linéaire (0.7432 vs 0.7433 vs 0.7433).

**Interprétation — un mini-théorème empirique** : pour un récepteur à prédicats de seuil, le coût d'explicabilité est **invariant aux déformations monotones coordonnée-par-coordonnée** de sa base (un seuil se transporte à travers toute fonction monotone). Ce qui coûte, c'est le **mélange** des dimensions (la rotation), pas leur reparamétrisation. Le désalignement pertinent est donc structurel (quelles directions se mélangent), pas métrique. À énoncer comme proposition formelle dans l'article — c'est un résultat négatif qui précise le concept.

## 9. Expérience 4 — L'explicabilité dépend de la question Q

Protocole : sur le graphe de référence de M, taille de la réponse contrastive « pourquoi a plutôt que b ? » = nombre minimal de prédicats divergents entre le chemin de l'instance et le plus proche chemin menant à b, pondéré par la couverture des feuilles.

| Question Q | Taille moyenne de la réponse |
|---|---|
| pourquoi B plutôt que A ? | **2.95** prédicats |
| pourquoi C plutôt que A ? | 3.55 |
| pourquoi A plutôt que C ? | 4.00 |
| pourquoi C plutôt que B ? | 4.42 |
| pourquoi A plutôt que B ? | 5.81 |
| pourquoi B plutôt que C ? | **6.39** prédicats |

Le même modèle est deux fois plus « explicable » pour certaines questions que pour d'autres (2.95 vs 6.39), et la relation est **asymétrique** (A-vs-B = 5.81 mais B-vs-A = 2.95) — cohérent avec la théorie pragmatique : l'explication n'est pas symétrique dans le contraste. L'explicabilité complète Expl(M, R) doit donc être définie comme une espérance sur la distribution des questions Q du contexte d'usage : Expl(M, R, Q̄) = E_Q[taille de réponse].

## 10. Expérience 5 — Le contact avec le réel, versant négatif : German Credit

### 10.1 Protocole
- **Données réelles** : Statlog German Credit (UCI n°144), 1000 dossiers, 20 attributs (7 numériques, 13 catégoriels one-hot), cible binaire bon/mauvais crédit (70/30).
- **Modèle opaque M** : MLP 2×50 (protocole v0 enregistré) ; amendement documenté v0.1 : gradient boosting + 20 000 requêtes de distillation supplémentaires (bootstrap + bruit), après constat que le MLP v0 (accuracy 0.72 pour une classe majoritaire à 0.70) n'avait presque pas de structure à expliquer.
- **Vocabulaires du récepteur** : brut (features telles quelles) ; expert = brut + concepts composés du crédit (mensualité = montant/durée, charge = mensualité × taux de remboursement, exposition = montant × nb crédits) ; contrôle monotone (log montant, √durée, âge²), prédit inerte par l'Exp 1b.
- **Mesure** : courbes de fidélité (budgets 2 à 256 feuilles), AUC ; n = 10 seeds ; écarts appariés par seed (test t apparié, Wilcoxon). **Critère de falsification a priori** : écart AUC expert−brut < 1 écart-type inter-seeds ⇒ pas de désalignement naturel sur ces données.

### 10.2 Résultats

| Run (n = 10 seeds) | AUC brut | AUC expert | Écart apparié | t apparié | Wilcoxon |
|---|---|---|---|---|---|
| v0 (MLP) | 0.733 ± 0.025 | 0.727 ± 0.019 | −0.006 ± 0.018 | p = 0.32 | p = 0.48 |
| v0.1 (GBT + requêtes) | 0.803 ± 0.026 | 0.801 ± 0.021 | −0.002 ± 0.019 | p = 0.72 | p = 0.83 |

Contrôle monotone − brut : −0.0008 ± 0.0016 (v0) et 0.0000 (v0.1) — l'invariance de l'Exp 1b tient sur données réelles.

### 10.3 Interprétation
Le critère de falsification a parlé : **pas de dominance du vocabulaire expert sur German Credit** — infirmation propre, rapportée avec les mêmes honneurs que les confirmations. Deux lectures : (a) le signal prédictif de ce dataset vit dans des variables catégorielles (statut de compte, historique) partagées par les deux vocabulaires, et le concept expert central du crédit (ratio dette/revenu) n'y est pas calculable (pas de revenu dans les attributs) ; (b) plus profond : la dominance du vocabulaire expert exige que le processus générateur du monde soit lui-même écrit en grandeurs composées — ce qui motive l'Expérience 6. Leçon méthodologique incorporée aux protocoles suivants : rapporter la courbe d'explicabilité à la fidélité du modèle trivial (classe majoritaire de M), sans quoi un M sans structure rend le protocole muet.

## 11. Expérience 6 — Le contact avec le réel, versant positif : maintenance prédictive

### 11.1 Protocole
- **Données réelles** : AI4I 2020 Predictive Maintenance (UCI n°601), 10 000 points, 5 capteurs (T° air, T° process, vitesse de rotation, couple, usure d'outil). Les modes de défaillance du benchmark sont écrits en grandeurs composées : dissipation (ΔT et vitesse), puissance (couple × vitesse angulaire), surcontrainte (usure × couple). Classes : {aucune panne, HDF, PWF, OSF, modes résiduels}.
- **Hypothèse enregistrée a priori** : sur un terrain physique — où le processus générateur EST écrit en grandeurs composées — le vocabulaire de l'ingénieur (capteurs + ΔT, puissance, contrainte) domine le vocabulaire capteurs bruts. Même critère de falsification que l'Exp 5.
- **Mesure** : fidélité équilibrée par classe (les défaillances sont rares — leçon de l'Exp 5), budgets 2 à 256 feuilles, n = 10 seeds, tests appariés. Deux modèles opaques : MLP 2×50 et gradient boosting.

### 11.2 Résultats

| M (n = 10 seeds) | AUC brut | AUC ingénieur | Écart apparié | t apparié | Wilcoxon |
|---|---|---|---|---|---|
| **MLP** | 0.702 ± 0.050 | 0.748 ± 0.048 | **+0.046 ± 0.026** | **t = 5.37, p = 4.5×10⁻⁴** | **p = 0.002** |
| GBT | 0.760 ± 0.022 | 0.755 ± 0.017 | −0.005 ± 0.027 | p = 0.56 | p = 0.56 |

Contrôle monotone − brut ≈ 0 dans les deux cas (invariance, encore). Accuracy équilibrée de M : 0.62 (MLP), 0.71 (GBT) — les modes résiduels TWF/RNF d'AI4I sont quasi inapprenables, propriété connue du benchmark.

### 11.3 Interprétation
**Première démonstration du désalignement naturel des bases sur données réelles** (claim à conditionner à la vérification bibliographique). Avec l'Exp 5, un diptyque : pas de dominance là où le monde n'est pas écrit en concepts composés (crédit), dominance nette là où il l'est (physique) — le désalignement naturel existe, et le cadre prédit où. Le résultat GBT est la surprise structurelle : un ensemble d'arbres est fait de splits axis-aligned sur les features brutes — **sa base interne est le vocabulaire brut par construction** — et l'écart disparaît ; le MLP mélange les dimensions comme la physique le fait, et l'écart apparaît. Mêmes données, mêmes récepteurs, M différent → relation d'explicabilité différente : la thèse relationnelle observée **côté modèle**, tout le reste tenu fixe. Réserves : un seul dataset par verdict ; classes rares limitant la structure apprenable de M ; vocabulaires experts choisis par les auteurs, pas appris.

## 12. Expérience 7 — Le régime interactif : un graphe maintenu par dialogue sous dérive continue

### 12.1 Protocole (pré-enregistré, conditions de mort publiées avant le run — le dépôt git fait foi)
- Monde de référence G\* (5 attributs, section 5) subissant **15 dérives successives** : à chaque pas, la classe d'une branche change (schedule déterministe cyclique).
- **Compétiteurs** : (a) graphe explicable (32 feuilles distillées du M initial) maintenu par dialogue — UNE phrase par dérive (« dans la région ⟨condition de la branche⟩, c'est désormais la classe c »), interprétée sur l'expérience non étiquetée du récepteur (toute règle dont la région de tir est majoritairement dans la région de la phrase est re-classée) ; zéro exemple étiqueté ; (b) MLP figé ; (c) MLP fine-tuné (100 exemples étiquetés frais par dérive, 50 époques) ; (d) MLP réentraîné à neuf (5000 exemples par dérive). 5 seeds.
- **Variantes de stress** : phrases bruitées (seuils ± 0.05 et ± 0.10 — l'imprécision humaine) ; récepteur en base désalignée θ = 1.5 (le pont entre les Exp 1-2 et l'Exp 3).
- **Conditions de mort a priori** : K1 le graphe passe sous le fine-tuning sur les 5 dernières dérives ; K2 l'accuracy d'une région jamais éditée se dégrade après 15 éditions ; K3 l'avantage sur le modèle figé disparaît sous phrases bruitées ± 0.10 ; K4 le graphe désaligné tombe sous le modèle figé.

### 12.2 Résultats

| Méthode | Supervision totale (15 dérives) | Accuracy moyenne (dérives 1-15) |
|---|---|---|
| MLP figé | — | 0.624 ± 0.002 |
| MLP fine-tuné | 1 500 étiquettes | 0.854 ± 0.018 (dents de scie d'oubli, min 0.740) |
| MLP réentraîné à neuf | 75 000 étiquettes | 0.981 ± 0.002 |
| **Graphe + dialogue** | **15 phrases, 0 étiquette** | **0.990 ± 0.003** |
| Graphe, phrases bruitées ± 0.05 | 15 phrases | 0.984 ± 0.008 |
| Graphe, phrases bruitées ± 0.10 | 15 phrases | 0.971 ± 0.018 |
| Graphe, base désalignée θ = 1.5 | 15 phrases | 0.801 ± 0.028 |

Les quatre conditions de mort ont survécu. Intégrité de la région jamais éditée après 15 éditions : 0.992 → 0.994 (**zéro dégradation cumulative**). Contrôle non planifié : le schedule cyclique ramène le monde à son état initial à la dérive 12, où le modèle figé remonte exactement à son niveau d'origine — la mécanique de dérive est saine.

### 12.3 Interprétation
**Quinze phrases sans aucune étiquette font mieux que soixante-quinze mille étiquettes de réentraînement.** L'Exp 3 montrait une édition ; l'Exp 7 montre le régime : sous dérive continue, le canal sémantique domine durablement le gradient, sans oubli cumulatif (K2 : la localité tient sur 15 éditions), en encaissant l'imprécision humaine (± 0.10 ne coûte que ~2 points), et en payant une **taxe d'expressibilité mesurée (~0.19)** quand la base est désalignée — reliant quantitativement les Exp 1-2 à l'Exp 3. Formulation à employer (conjecture assumée, inchangée depuis la section 3.3) : l'apprentissage par édition de graphe en dialogue est un **paradigme candidat post-gradient**. Limites propres : le monde est compressible par construction et le récepteur possède le bon biais inductif (régime aligné — la variante θ = 1.5 chiffre le cas contraire) ; la phrase localise la règle à corriger (la localisation autonome — algorithme A1 — reste ouverte).

## 13. Limites (à écrire honnêtement)
- Données synthétiques basse dimension ; G\* connu par construction. C'est un choix (contrôle total du désalignement, impossible avec des humains), mais la généralisation à haute dimension et données réelles reste à démontrer.
- Récepteurs artificiels ; la validation humaine (experts vs novices comme bases différentes) est l'étape suivante, pas la présente contribution.
- Le désalignement est modélisé par rotation linéaire ; les désalignements conceptuels réels sont non linéaires.
- Le proxy « graphe de M » = arbre distillé haute fidélité, non le réseau exact.
- Exp 3 : la comparaison dialogue/fine-tuning n'est pas à information égale (assumé, c'est la thèse), et l'identification de la règle à éditer est ici assistée par la connaissance de G\* ; en conditions réelles, la localisation de la règle fautive est un problème en soi.
- Trade-off performance/interprétabilité (Rudin) : nos mondes synthétiques sont compressibles par construction ; la thèse « le graphe interactif bat le réseau figé en régime d'apprentissage continu » est maintenant testée en régime synthétique (section 12), pas encore sur flux réels.
- Exp 5-6 : un seul dataset par verdict du diptyque ; les vocabulaires experts sont choisis par les auteurs, pas appris ; sur AI4I, les modes résiduels quasi aléatoires limitent la structure apprenable de M.
- Exp 7 : les phrases proviennent d'un oracle qui localise la région concernée (variantes bruitées testées, localisation autonome non résolue — A1) ; le récepteur a le biais inductif du monde.

## 14. Roadmap (section future work)
1. ~~Exp 3 — l'opérateur inverse~~ **FAIT** (section 7) : 1 phrase de dialogue = 0.990, > 3000 exemples de fine-tuning.
2. ~~Désalignements non linéaires~~ **FAIT partiellement** (section 8) : invariance aux déformations monotones établie ; reste les désalignements conceptuels appris (concept bottleneck, CKA avec représentations humaines).
3. Validation humaine : simulatability mesurée sur sujets, bases opérationnalisées par expertise (experts vs novices). Non exécutable in silico — première priorité post-publication.
4. Compression contextuelle de LLM : « le meilleur graphe de taille K pour le contexte C » comme primitive. Exige infrastructure LLM.
5. ~~Distribution de questions Q~~ **FAIT** (section 9) : hétérogénéité (2.95→6.39) et asymétrie du contraste démontrées ; reste à pondérer par une distribution de Q réaliste.
6. Nouveau, issu de l'Exp 3 : mécanisme d'édition quand la correction n'est PAS exprimable dans le vocabulaire partagé (le cas désaligné) — le pont entre Exp 1-2 et Exp 3.
7. Nouveau, issu de l'Exp 1b : preuve formelle de l'invariance monotone et caractérisation du coût par la structure de mélange (angle entre sous-espaces). L'invariance est maintenant confirmée empiriquement sur 11 runs (synthétiques et réels) — la preuve est à rédiger.
8. ~~Validation sur données réelles~~ **FAIT** (sections 10-11) : diptyque German Credit (infirmation propre) / AI4I (dominance, p = 4.5×10⁻⁴), modéré par la base interne de M — reste : plus de datasets par verdict, vocabulaires experts appris plutôt que choisis.
9. ~~Régime d'apprentissage continu~~ **FAIT en synthétique** (section 12) : 15 phrases > 75 000 étiquettes sous dérive, zéro oubli cumulatif — reste : flux de drift réels (Electricity/Airlines) et localisation autonome (A1).
10. Nouveau, issu du recul sur les fondamentaux (perspectives d'une ligne, ne pas développer dans ce papier) : base commune construite par boucle rétroactive bilatérale sous politiques de mise à jour ; flou du langage comme superposition de graphes nets ; opérateur de calibration W_cal.

## 15. Matériel reproductible
- `exp1_solid.py` : expérience 1 (10 seeds, rotations expm(θA), courbes et AUC).
- `exp2.py` : expérience 2 (opérateur W, dialogue actif, deux récepteurs).
- `exp3.py` : expérience 3 (opérateur inverse : édition de graphe vs fine-tuning).
- `exp1b_exp4.py` : expériences 1b (désalignement non linéaire) et 4 (dépendance à Q).
- `exp5_german_credit.py` : expérience 5 (German Credit ; `--seeds`, `--model`, `--augment` ; stats appariées).
- `exp6_predictive_maintenance.py` : expérience 6 (AI4I 2020 ; fidélité équilibrée ; `--simulate` pour la validation sans données).
- `exp7_living_graph.py` : expérience 7 (15 dérives, 4 compétiteurs, variantes bruit/désalignement, conditions de mort évaluées).
- Librairie `core/rex` (RuleListModel, W, W⁻¹, métriques) + tests unitaires dont l'invariant de localité de l'édition.
- Figures : `exp1_courbes.png`, `exp2_dialogue.png`, `exp3_dialogue_vs_finetuning.png`, `exp5_german.png`, `exp6_ai4i.png`, `exp7_living_graph.png`.
- Données : scripts de téléchargement dans `/data` (German Credit UCI n°144 ; AI4I 2020 UCI n°601) — aucune donnée commitée.
- Environnement : Python, numpy, scikit-learn, scipy. Seeds fixées, tous les chiffres cités reproduits de zéro (Exp 1-4 : reproduction vérifiée à l'identique le 2026-07-06).

## 16. Consignes pour l'assistant rédacteur
- La vision et l'approche sont posées par l'auteur (Reda) ; ne pas les altérer, les mettre en forme.
- Format : position paper (4-8 pages) — vision assumée, résultats présentés comme preuve de concept, limites explicites.
- Ton : ambitieux sur le cadre, sobre sur les preuves. Chaque claim empirique doit pointer vers les tableaux ci-dessus.
- Compléter les citations exactes (références section 4.5), vérifier les années.
- Ne pas sur-vendre : pas de claim sur les humains ; les claims sur données réelles se limitent strictement aux tableaux des sections 10-12 (mise à jour 2026-07-06 : le diptyque réel et le régime interactif sont désormais acquis et citables).
- L'abstract (section 2) doit être mis à jour pour couvrir les sections 10-12 — **proposition à valider par Reda, ne pas publier sans son accord** : ajouter après « seule la base du récepteur change » : « Au contact de données réelles, le cadre prédit où le désalignement naturel apparaît : absent sur un jeu de crédit dont les concepts experts ne portent pas le signal (infirmation propre, pré-enregistrée), net sur un benchmark de maintenance prédictive dont les lois sont écrites en grandeurs composées (+0.046, p < 10⁻³) — et modulé par la base interne du modèle lui-même. Enfin, sous dérive continue, un graphe maintenu par dialogue (une phrase par dérive, zéro étiquette) surpasse un réseau réentraîné avec 75 000 exemples, sans oubli cumulatif — l'apprentissage par édition comme paradigme candidat post-gradient. »
