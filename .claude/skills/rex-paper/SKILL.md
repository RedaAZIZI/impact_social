---
name: rex-paper
description: Rédiger ou mettre à jour le papier REX (position paper explicabilité relationnelle) et préparer les soumissions (arXiv, workshops). Utiliser quand l'utilisateur demande de rédiger/mettre à jour le papier ou préparer une soumission.
---

# Rédaction du papier REX

**Statut depuis le 2026-07-06** : le papier v1 (preprint arXiv, `/paper`) a été refusé en
review et ne se resoumet PAS en l'état (décision dans `docs/STRATEGIE.md`). Le preprint
reste publié (drapeau de priorité). **La v2 se construit sur l'axe REX-Géo** : thèse des
invariants, théorèmes T1/T2 (`docs/preuves_invariance.md`), noyau de relations
(`docs/noyau_geometrique_v0.1.md`), Exp 1-7 relues comme mesures de l'invariant, ancrages
dans `docs/REVUE_LITTERATURE.md`. Règle de recyclage : rien de v1 n'entre dans v2 sans
relecture géométrique explicite. Plan v2 : issue Linear X-49.

Source de vérité v1 : `docs/article_source_explicabilite.md` (vision, cadre formel, protocoles, tableaux de résultats complets, biblio). Sources LaTeX dans `/paper`.

## Consignes intangibles (section 13 du document source)

1. **La vision et l'approche sont posées par l'auteur (Reda) : ne pas les altérer, les mettre en forme.**
2. Ton : **ambitieux sur le cadre, sobre sur les preuves**.
3. Chaque claim empirique pointe vers un tableau de résultats (sections 5-9 du document source). Pas de chiffre sans source.
4. **Ne pas sur-vendre** : aucun claim sur données réelles ni sur humains tant que ce n'est pas fait. La section Limites (section 10) est explicite et honnête.
5. L'apprentissage par édition (Exp 3) se formule en **conjecture assumée**, pas en claim établi : « Nous conjecturons que l'apprentissage par édition de graphe en dialogue constitue un paradigme candidat pour l'apprentissage post-gradient… »
6. Le lien preuves interactives/debate reste une perspective d'une ligne (pas de section).

## Format cible

- Preprint arXiv : position paper 6-8 pages, cs.LG, cross-list cs.AI.
- Workshops visés : interpretability NeurIPS/ICML, XAI World (vérifier les deadlines dans Linear, projet REX-P1).

## Références (section 4.5 du document source — vérifier années et auteurs exacts)

CKA (Kornblith et al., 2019) ; Doshi-Velez & Kim (2017) ; Hase & Bansal (2020) ; van Fraassen, *The Scientific Image* (1980) ; Miller (2019) ; Wachter et al. (2017) ; Frosst & Hinton (2017) ; TREPAN (Craven & Shavlik, 1996) ; Angluin (1988) ; Rudin (2019) ; McCloskey & Cohen (1989) ; French (1999) ; EWC (Kirkpatrick et al., 2017) ; ROME (Meng et al., 2022) ; MEMIT (Meng et al., 2023) — s'en différencier : ils éditent des poids opaques via des heuristiques fragiles, ici on édite une structure explicable via le canal même de l'explication ; Machine teaching (Zhu, 2015).

## Chiffres clés à ne pas déformer

AUC 0.918 (θ=0) → 0.745 (θ=1.5) ; 6 questions → 92 % aligné vs plafond ~71 % désaligné ; édition 1 phrase = 0.990 vs fine-tuning 3000 exemples = 0.968 ; invariance monotone (AUC 0.743 identique) ; taille contrastive 2.95 → 6.39 selon Q.
