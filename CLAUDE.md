# REX — contexte projet pour Claude

## Ce qu'est ce projet

Recherche : **REX (Relational Explainability)**, pivotée le 2026-07-06 vers l'axe
**REX-Géo** — une théorie géométrique-ordinale des concepts et de la langue :
- les concepts sont des formes (régions nommées) dans un produit de dimensions ordonnées ;
- le groupe d'invariance G (déformations monotones par axe) définit la géométrie
  (lecture Erlangen) — mesuré expérimentalement par l'Exp 1b ;
- **thèse candidate** : la langue qualitative parle dans les invariants de ce groupe
  (comparatifs, inclusions, précédences = le noyau de relations ℛ) ; l'explicabilité est
  la géométrie de ce transfert ; W_cal calibre ce que l'invariance ne transporte pas ;
- étoile polaire produit : une base de connaissance relationnelle requêtable et
  maintenable par phrases (W lit, W⁻¹ écrit, W_cal calibre).

Le corpus v1 (Exp 1-7, preprint arXiv dans `/paper`) est la **fondation empirique** —
conservé intégralement, jamais resoumis tel quel (refusé en review), recyclé uniquement
avec relecture géométrique explicite.

## Ordre de lecture pour se mettre en contexte

1. `docs/STRATEGIE.md` — décisions (en particulier « Décision du 2026-07-06 »).
2. `docs/noyau_geometrique_v0.1.md` — la théorie (Déf/T/P/C, faits nécessaires F1-F7).
3. `docs/preuves_invariance.md` — théorèmes T1/T2 et leurs limites.
4. `docs/FONDAMENTAUX.md` — sessions 1-10 : intuitions de Reda + garde-fous A-G1→A-G19
   (normatifs : ils contraignent tout design futur).
5. `docs/REVUE_LITTERATURE.md` — ancrages, références vérifiées, risques de collision.

## Méthode de travail (non négociable)

- **Méthode maison** : Reda énonce une intuition (souvent en vocal, transcription
  bruitée) ; l'assistant raffine, joue l'avocat du diable, consigne dans FONDAMENTAUX
  (énoncé brut → formulation raffinée → attaques → grandeurs mesurables → questions).
- **Discipline** : hypothèse et critère de falsification AVANT toute expérience ;
  multi-seeds ; pré-enregistrement ; rien n'est codé tant qu'un document ne le force
  pas ; aucun appel API payant sans go de Reda palier par palier.
- **Honnêteté** : les infirmations se publient (Exp 5) ; pas de survente.

## Organisation

- **Linear** : initiative « REX — Explicabilité relationnelle » ; projet actif
  **REX-Géo — Le noyau de relations** (team Engineering, issues X-42→X-49) ;
  REX-Lab (labo conversationnel) et REX-LLM (Exp 8, en pause) restent rattachés.
  Les projets non liés à la recherche sont annulés dans la team Engineering.
- **Skills projet** : `rex-geo-theorie` (théorie du pivot — commencer là),
  `rex-experiment` (protocole d'expérience), `rex-core-dev` (librairie /core),
  `rex-paper` (rédaction).
- **Tests** : `python -m pytest tests/` doit rester 10/10 vert ; l'invariant de
  localité de l'édition est non négociable.

## Prochaines actions (état au 2026-07-06, fin de session fondatrice)

1. **I1** (X-43) : grammaire du fragment invariant = spécification du noyau ℛ — verrou
   du programme I, fondée sur T2.
2. Intégrer les verdicts de la relecture adverse des preuves (X-42), puis LaTeX.
3. **F5** (X-45) : première expérience du nouveau programme (saillance, coût nul,
   pré-enregistrement obligatoire).
4. F4 (X-47), F7 (X-46), puis I2/I3 (X-48) et plan v2 du papier (X-49).
