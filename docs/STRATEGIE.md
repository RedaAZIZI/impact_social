# Stratégie du projet « Explicabilité relationnelle » — décision et plan d'exécution

**Décision : académique d'abord, produit en veille active.**
Justification : le risque scientifique (validité sur données réelles) est bloquant et bon marché à lever ; le risque produit est cher et dépend du premier. La recherche définira le produit (la boucle W/W⁻¹ EST le futur moteur du produit), pas l'inverse.

---

## Phase 1 — Planter le drapeau (semaines 1-4)

Objectif : priorité intellectuelle datée + infrastructure de recherche propre.

**Livrables :**
1. **Preprint arXiv** (cs.LG / cs.AI) — à partir de `article_source_explicabilite.md`. Format position paper, 6-8 pages. C'est le document qui date l'idée.
2. **Repo GitHub public** `impact_social` (nom conservé, décision du 2026-07-06) :
   - `/paper` — sources LaTeX du preprint
   - `/experiments` — exp1_solid.py, exp2.py, exp3.py, exp1b_exp4.py (+ seeds, requirements.txt)
   - `/figures` — les 3 PNG
   - `/core` — première librairie : RuleListModel, extract_rule (W), edit (W⁻¹), fidelity_curve — le début du futur moteur produit
   - README avec les 3 résultats clés en tête, LICENSE (MIT ou Apache-2 pour usage industriel futur)
3. **Ce document de stratégie** (suivi des décisions).

## Phase 2 — Lever le risque scientifique (mois 1-3)

Objectif : valider/infirmer sur données réelles + modélisation mathématique complète.

**Volet expérimental :**
1. German Credit / Heart Disease (UCI) : désalignement naturel features brutes vs concepts experts (IMC, ratio dette/revenu). Courbes d'explicabilité dans les deux vocabulaires. **Critère go/no-go : le vocabulaire expert domine-t-il la courbe ?**
2. Boucle W/W⁻¹ complète sans assistance : l'utilisateur signale « mal classé », le système localise la règle fautive, propose l'édition, l'utilisateur valide. Algorithme à concevoir (voir volet théorique). Benchmark de drift : Electricity/Airlines.
3. Benchmark continual learning : édition de graphe vs EWC / replay / LoRA — le résultat « zéro régression par construction ».

**Volet théorique (la modélisation mathématique demandée) :**
- Définition axiomatique : Expl(M, R, Q, ε) ; propriétés exigées de W (minimalité, traduisibilité, composabilité) énoncées comme axiomes.
- **Proposition 1** (issue de l'Exp 1b) : invariance du coût d'explicabilité aux déformations monotones coordonnée-par-coordonnée ; le coût est fonction de la structure de mélange (angles principaux entre sous-espaces). À prouver.
- **Proposition 2** : bornes sur le nombre de questions W pour reconstruire M à fidélité ε (pont avec l'exact learning d'Angluin ; W = requête plus riche qu'une membership query → borne supérieure améliorée à établir).
- **Algorithme A1** (localisation de règle fautive) : étant donné un exemple signalé, trouver l'édition minimale du graphe qui corrige l'exemple sans changer les prédictions hors de la région — formuler comme problème d'optimisation discrète, prouver la localité.
- **Définition de l'explicabilité contextuelle** : Expl(M, R, Q̄) = E_Q[taille de réponse contrastive] sur la distribution de questions du contexte d'usage.

**Livrable de phase : papier main track** (NeurIPS/ICML/ICLR) = cadre + théorie + données réelles + boucle complète.

## Phase 3 — Décision produit (mois 3-6, conditionnelle au go de la phase 2)

Ne démarre QUE si German Credit valide et si l'algorithme A1 fonctionne en conditions réelles.

**Livrables préparés d'avance (veille active, coût quasi nul) :**
- **Mémo produit 1 page** (déjà esquissé) : thèse « edge AI corrigeable en une phrase », les 4 tests produit (frugalité <50Mo/<50ms, correction <30s, zéro régression, adaptation au drift), et le domaine d'attaque n°1 : à définir — cap deep tech (IA embarquée corrigeable en une phrase), sans verticale métier privilégiée à ce stade.
- La `/core` du repo devient le moteur : chaque avancée de recherche est du code produit gratuit.
- Démo cible : 90 secondes, correction vocale d'un modèle sur téléphone, effet immédiat, zéro régression démontrée en direct.

## Ce qu'on ne fait PAS maintenant (discipline anti-dispersion)
- Pas de développement produit avant le go de phase 2.
- Pas de CUB-200/vision avant que le tabulaire soit conclu (extension, pas fondation).
- Pas de lien preuves interactives/debate dans le papier (perspective d'une ligne).
- Pas de levée de fonds ni de pitch avant la démo de phase 3.

## Prochaine action immédiate
1. Structurer le repo GitHub (squelette + code existant + README).
2. Passer `article_source_explicabilite.md` en LaTeX arXiv.
3. Lancer le pipeline German Credit.
