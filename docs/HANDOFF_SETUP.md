# HANDOFF — Configuration de l'environnement projet « Explicabilité relationnelle »

Document destiné à l'IA de setup. Objectif : créer l'espace Linear, le repo GitHub et les skills pour faire naître le projet. Tout le contexte scientifique et stratégique est dans les fichiers joints ; ne pas réinventer, configurer.

---

## 0. Fichiers sources de référence (à importer dans le projet)
- `article_source_explicabilite.md` — vision, cadre formel, 4 expériences, résultats, biblio, consignes de rédaction.
- `STRATEGIE.md` — décision (académique d'abord), 3 phases, critères go/no-go, anti-dispersion.
- Code : `exp1_solid.py`, `exp2.py`, `exp3.py`, `exp1b_exp4.py`.
- Figures : `exp1_courbes.png`, `exp2_dialogue.png`, `exp3_dialogue_vs_finetuning.png`.

## 1. Identité du projet
- **Nom** : Relational Explainability (nom de code : REX)
- **One-liner** : L'explicabilité n'est pas une propriété du modèle mais de la relation modèle-récepteur ; on la mesure, et le même canal sert à corriger le modèle en une phrase.
- **Owner** : Reda (vision, direction scientifique, arbitrages).
- **Résultats déjà acquis** (v0, monde synthétique) : coût d'explicabilité monotone en le désalignement des bases (AUC 0.918→0.745) ; reconstruction par 6 questions « pourquoi » en base alignée vs non-convergence en base désalignée ; 1 phrase d'édition = 0.990 vs 3000 exemples de fine-tuning = 0.968.

## 2. Configuration Linear

### 2.1 Structure
- **Initiative** : « REX — Explicabilité relationnelle »
- **3 projets** (mappés sur les phases de STRATEGIE.md) :
  1. `REX-P1 — Drapeau` (target : +4 semaines)
  2. `REX-P2 — Risque scientifique` (target : +3 mois)
  3. `REX-P3 — Produit (conditionnel)` (pas de date ; statut backlog, gelé jusqu'au go de P2)

### 2.2 Labels
`paper` · `code` · `theory` · `experiment` · `infra` · `produit` · `go/no-go`

### 2.3 Backlog initial (créer ces issues)

**Projet P1 — Drapeau**
| Titre | Label | Priorité | Description courte |
|---|---|---|---|
| Créer repo GitHub `relational-explainability` (squelette section 3) | infra | Urgent | Structure, LICENSE Apache-2, requirements.txt, CI lint |
| Migrer les 4 scripts d'expériences + seeds dans `/experiments` | code | Urgent | Reproductibilité vérifiée de zéro (fresh clone → figures identiques) |
| Extraire la librairie `/core` : RuleListModel, W (extract_rule), W⁻¹ (edit), fidelity_curve | code | High | Le futur moteur ; API documentée, tests unitaires |
| README avec les 3 résultats clés + figures | infra | High | — |
| Conversion de l'article source en LaTeX (template arXiv, 6-8 p.) | paper | Urgent | Suivre section 13 du doc source ; ne pas altérer la vision |
| Compléter et vérifier les références biblio (section 4.5 + 3.3) | paper | High | Années, auteurs exacts |
| Soumission arXiv (cs.LG, cross-list cs.AI) | paper | Urgent | Date la priorité intellectuelle |
| Identifier 2-3 workshops cibles (NeurIPS/ICML interpretability, XAI World) + deadlines | paper | Medium | — |

**Projet P2 — Risque scientifique**
| Titre | Label | Priorité | Description courte |
|---|---|---|---|
| Pipeline German Credit / Heart Disease : features brutes vs concepts experts | experiment | Urgent | Vocabulaire expert = IMC, ratio dette/revenu, pression pulsée… |
| **GO/NO-GO : le vocabulaire expert domine-t-il la courbe d'explicabilité ?** | go/no-go | Urgent | Critère défini dans STRATEGIE.md ; décision documentée |
| Algorithme A1 : localisation de la règle fautive depuis un simple signalement | theory | High | Formuler en optimisation discrète ; prouver la localité |
| Implémentation boucle W/W⁻¹ complète sans assistance | code | High | Dépend de A1 |
| Benchmark drift (Electricity/Airlines) : boucle dialogue vs réentraînement | experiment | Medium | — |
| Benchmark continual learning : édition vs EWC/replay/LoRA (zéro régression) | experiment | Medium | — |
| Proposition 1 : preuve de l'invariance monotone / coût = structure de mélange | theory | Medium | Angles principaux entre sous-espaces |
| Proposition 2 : bornes sur le nb de questions W (pont Angluin) | theory | Medium | — |
| Rédaction papier main track | paper | Low (fin de phase) | Cadre + théorie + réel + boucle |

**Projet P3 — Produit (gelé)**
| Titre | Label | Priorité |
|---|---|---|
| Mémo produit 1 page (edge AI corrigeable ; 4 tests : <50Mo/<50ms, correction <30s, zéro régression, drift) | produit | Backlog |
| Étude niche conformité EU AI Act fintech (terrain Anaxago) | produit | Backlog |
| Spec démo 90s : correction vocale on-device, effet immédiat | produit | Backlog |

### 2.4 Règles de gestion
- Rien ne passe de P3 en actif sans une issue `go/no-go` de P2 fermée en GO, décision par Reda.
- Toute expérience = une issue avec : hypothèse, critère de falsification a priori, seeds, lien commit.
- La section « ce qu'on ne fait PAS » de STRATEGIE.md fait foi en cas d'arbitrage.

## 3. Repo GitHub `relational-explainability`
```
/paper          # LaTeX arXiv
/experiments    # exp1_solid.py, exp2.py, exp3.py, exp1b_exp4.py, seeds, README par exp
/figures        # les 3 PNG
/core           # rex/ : models.py (RuleListModel), why.py (W), edit.py (W⁻¹), metrics.py (courbes, AUC)
/tests          # tests unitaires de /core
/data           # scripts de téléchargement UCI (pas de données commitées)
README.md · LICENSE (Apache-2) · requirements.txt · CITATION.cff
```
Conventions : Python 3.12, numpy/sklearn/scipy uniquement en phase 1-2 ; chaque script reproduit ses figures de zéro ; seeds fixées partout.

## 4. Skills à créer (pour les futures sessions IA)

**Skill 1 — `rex-experiment`**
Déclencheurs : « lance/design une expérience REX », « teste l'hypothèse… »
Contenu : le protocole standard (hypothèse écrite AVANT, critère de falsification, multi-seeds ≥5, moyenne±std, figure matplotlib, mise à jour de l'article source, issue Linear liée) ; le monde synthétique de référence (G\*, 5 attributs, MLP 2×50) ; les définitions (Expl(M,R,Q,ε), courbe d'explicabilité, AUC).

**Skill 2 — `rex-paper`**
Déclencheurs : « rédige/mets à jour le papier », « prépare la soumission »
Contenu : consignes de la section 13 de l'article source (vision de Reda intouchable, ton ambitieux sur le cadre / sobre sur les preuves, claims → tableaux, limites explicites) ; état des références ; formats cibles (arXiv, workshops).

**Skill 3 — `rex-core-dev`**
Déclencheurs : « développe/refactore le moteur », « ajoute à /core »
Contenu : API de la librairie, invariants à préserver (l'édition doit rester locale par construction — un test le vérifie), style, politique de dépendances minimales.

## 5. Définition du succès à 3 mois
1. Preprint arXiv en ligne, repo public reproductible.
2. Issue go/no-go German Credit fermée (dans un sens ou l'autre — une infirmation propre est un succès de méthode).
3. Algorithme A1 spécifié et prototypé.
4. Zéro travail produit effectué hors du mémo 1 page.
