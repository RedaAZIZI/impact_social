# REX — Explicabilité relationnelle · Mémoire de projet

Si Reda dit « continue le projet REX » : lis ce fichier, puis `docs/BILAN_DRAPEAU.md`
(état des résultats) et `docs/FONDAMENTAUX.md` (état de la pensée), consulte Linear,
et reprends au chemin critique (§ Prochaines actions) sauf directive contraire.

## Identité

- **Thèse** : l'explicabilité n'est pas une propriété du modèle M mais de la relation
  (M, R, Q) — récepteur et question comprises. Le même canal sert à expliquer (opérateur W)
  et à apprendre (W⁻¹, édition locale, zéro oubli par construction).
- **Owner** : Reda (vision, direction scientifique, arbitrages, budget). L'assistant
  exécute, formalise, challenge — mais la vision est celle de Reda et ne s'altère pas.
- **Cap produit** : deep tech (IA embarquée corrigeable en une phrase). PAS de verticale
  fintech, PAS d'Anaxago (correction explicite de Reda).
- **Langue de travail** : français. Auteur du papier : Reda Azizi seul (IA en
  acknowledgments — les venues interdisent une IA co-autrice).

## Où tout vit

- `docs/article_source_explicabilite.md` — source de vérité du papier (sections 1-4 vision
  INTOUCHABLE ; 5-12 expériences ; 13-16 limites/roadmap/matériel/consignes).
- `docs/BILAN_DRAPEAU.md` — inventaire chiffré complet + plan du preprint + décisions.
- `docs/FONDAMENTAUX.md` — le recul sur l'intuition (4 sessions : boucle rétroactive et
  politiques π ; superposition de graphes ; opérateur W_cal + 4 expériences E1-E4 de
  pensée ; embedding à la frontière + croissance du vocabulaire). Juge de paix des designs.
- `docs/noyau_formel_explicabilite_v0.1.md` — théorie (loi θ, pont statique↔interactif C3,
  Def 1.6 repère intrinsèque) → papier 2, cible TMLR (Linear S-70).
- `docs/EXP8_PROGRAMME.md` — programme REX-LLM (distiller un LLM), v2, EN PAUSE de recul.
- `core/rex/` — la librairie (RuleListModel, W, W⁻¹, métriques) ; `tests/` (10 tests, dont
  l'invariant de localité — doit TOUJOURS rester vert).
- `experiments/` — exp1-4 (synthétique, reproduits à l'identique), exp5 (German Credit,
  infirmation propre), exp6 (AI4I, dominance réelle), exp7 (graphe qui vit, pré-enregistré),
  exp_e1_collapse + exp_e1bis (analyses du noyau formel). Résultats dans results/ (gitignoré).
- `lab/` — REX Lab : `rex_lab.html` (v0 curseurs, monde G★) et `rex_lab_conversation.html`
  (v0.2 conversationnel, jugement social/émotions, panneau d'intelligence).
  Artifacts publiés : v0 https://claude.ai/code/artifact/ada9a0cb-b6bb-4cd3-af43-5984817c8bab ·
  conversationnel https://claude.ai/code/artifact/39b62b96-ea13-4ef2-b28e-29276a786c82
- **Linear** : initiative « REX — Explicabilité relationnelle ». Team **Strategy** (S-xx) =
  REX-P1 Drapeau, REX-P2 Risque scientifique, REX-P3 Produit (gelé). Team **Engineering**
  (X-xx) = REX-LLM (pause) et REX-Lab (actif). Règle : toute expérience = hypothèse +
  falsification a priori (pré-enregistrement Linear/git AVANT le run).

## État au 2026-07-06 (fin de session fondatrice)

**Acquis scientifiques** : corpus v0 (Exp 1-4) reproduit de zéro à l'identique ; diptyque
réel — German Credit infirmation propre (−0.006±0.018, p=0.32, n=10) / AI4I dominance
(+0.046±0.026, t=5.37, p=4.5×10⁻⁴), modulée par la base interne de M (GBT : écart nul) ;
Exp 7 pré-enregistrée « 15 phrases > 75 000 étiquettes », 4 conditions de mort survécues ;
Prop 1 (invariance monotone) 11/11 ; loi θ du noyau confirmée dans son régime 2D
(symétrie 45° ✓, max à 45° ✓), forme naïve non transférable en 5D (exposant universel
−0.21 → chantier C4.3).

**Fait** : PR #1 mergée dans main (264974e). Cartes Done : S-54, S-55, S-56, S-61, S-74,
S-75. Décisions actées : titre « Explainability is Relational… » ; périmètre = v0 + réel ;
repo reste `impact_social` ; arXiv géré par Reda plus tard (checklist dans S-59).

**En pause** : REX-LLM (X-29…X-35) — aucun appel API sans GO explicite de Reda par
commentaire sur l'issue du palier. Budget plafond 100 €. MAIS : point d'entrée motivé
retrouvé = LLM-transducteur du labo (X-40).

**Chantier vivant** : REX-Lab. v0.2.1 en ligne. Limite constatée en usage réel : le graphe
ne fait que classifier et le texte libre n'entre pas (lexique pauvre). Direction de Reda :
couche de langue complète — transducteur texte→concepts + croissance du vocabulaire par
résidus nommés (X-40, FONDAMENTAUX session 4). Garde-fou : l'embedding vit à la frontière,
JAMAIS dans le graphe.

## Prochaines actions (ordre recommandé)

1. **S-57 — LaTeX du preprint** (chemin critique du drapeau) : convertir l'article source
   (16 sections) en position paper arXiv 6-8 p., 4 figures (exp1_courbes, exp2_dialogue,
   exp6_ai4i, exp7_living_graph). Puis S-58 (biblio exacte) → relecture Reda → S-59 (arXiv,
   par Reda). L'abstract étendu attend sa validation (article source §16).
2. **Lab : le graphe qui questionne** (X-40, sortie n°2 — sans API) : quand des facteurs
   sont inconnus, poser LA question discriminante. Transforme la classification en
   conversation avec la mécanique existante.
3. **E3 du noyau formel** (S-70) : diagnostic du plateau 71 % (informationnel vs
   budgétaire) — décisif pour le papier 2.
4. **Transducteur LLM** (X-40) : attend le GO budget de Reda.

## Règles de travail (ne pas violer)

- Vision de Reda intouchable ; ton ambitieux sur le cadre, sobre sur les preuves ; chaque
  claim pointe vers un tableau ; les infirmations se publient avec les mêmes honneurs.
- Pré-enregistrer avant de mesurer ; documenter tout amendement ; contrôle monotone
  systématique ; fidélité équilibrée quand classes rares ; vérifier la structure de M.
- Aucun appel API payant sans GO explicite ; aucune donnée personnelle ; datasets jamais
  commités (réseau sortant restreint : UCI/OpenML/HF bloqués — Reda dépose les fichiers).
- `python -m pytest tests/` avant tout commit touchant core/ ; l'invariant de localité est
  non négociable. Commits en anglais, travail sur la branche désignée, push + PR.
- Tout consigner : git (le protocole AVANT les résultats), Linear (état réel, liens
  commits), FONDAMENTAUX (les intuitions de Reda, sessions numérotées).
