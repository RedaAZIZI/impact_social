---
name: rex-geo-theorie
description: Travailler la théorie de la nouvelle direction REX-Géo (géométrie ordinale, fragment invariant, noyau de relations ℛ, contexte, preuves T1/T2, grammaire I1). Utiliser quand l'utilisateur demande de prouver/étendre un théorème, rédiger la grammaire du fragment, formaliser le contexte, ou attaquer un fait nécessaire F1-F7.
---

# Théorie REX-Géo — le noyau de relations

**Axe principal du projet depuis la décision du 2026-07-06** (voir `docs/STRATEGIE.md`,
section « Décision du 2026-07-06 — le pivot géométrique »).

## Documents source (ordre de lecture)

1. `docs/noyau_geometrique_v0.1.md` — LA référence : géométrie ordinale produit (X, G),
   fragment invariant, canal, contexte (K1/K2/K3), noyau ℛ (§8), résolution/fermeture/
   diagonale/dynamique (§9), faits nécessaires F1-F7.
2. `docs/preuves_invariance.md` — T1 (invariance du coût, ex-Prop 1) et T2
   (caractérisation du fragment invariant) avec limites L1-L4.
3. `docs/FONDAMENTAUX.md` sessions 5-10 — les intuitions de Reda, le raffinage, les
   attaques d'avocat du diable A-G1 → A-G19 (les garde-fous sont NORMATIFS).
4. `docs/REVUE_LITTERATURE.md` — ancrages et risques de collision.
5. Le noyau formel v0.1 (`docs/noyau_formel_explicabilite_v0.1.md`) — notations héritées
   (Expl_D, V_R, W, W⁻¹, θ) ; ne pas les redéfinir.

## Règles non négociables

1. **Méthode maison** : Reda énonce l'intuition ; l'assistant raffine ET joue l'avocat
   du diable ; tout survit ou meurt par attaque explicite, consignée dans FONDAMENTAUX.
2. **Toute affirmation géométrique se réduit à un invariant mesurable** (A-G1).
   « Riemannien » et « onde » n'entrent dans aucun document public sans mesure qui les
   force (A-G1, A-G17).
3. **Nommabilité** : les formes et relations restent des objets nommés ; aucun vecteur
   dans les nœuds, aucune relation apprise librement (A-G2, A-G13).
4. **Contexte** : trois crans K1/K2/K3 — on ne monte d'un cran que si une mesure y force
   (F4). La résolution ε_κ est pré-déclarée, jamais ajustée après jugement (A-G18).
5. **« Complet »** = clos sous les tables de composition (calculable), jamais au sens
   logique (A-G16). Vocabulaire : « réflexif », pas « conscient ».
6. **Statuts d'énoncés** : [T] prouvé · [P] proposition · [C] conjecture · [Déf] ·
   [F] fait nécessaire go/no-go. Ne pas promouvoir un [C] en [T] sans preuve rédigée et
   relue adversarialement.

## État des faits nécessaires (mise à jour à chaque avancée)

- F1, F2, F6 : preuves rédigées (T1, T2) dans `docs/preuves_invariance.md` — en attente
  de relecture adverse finale ; F6 réglé au niveau des configurations de points seulement.
- F3 (grammaire opérationnalisable) : bloqué par I1 (Linear X-43).
- F4 (cran de contexte) : à trancher par mesure (Linear X-47).
- F5 (prédiction saillance) : expérience à pré-enregistrer (Linear X-45).
- F7 (tables de composition médianes) : chantier ouvert (Linear X-46).

## Linear

Projet **REX-Géo — Le noyau de relations** (team Engineering, initiative REX).
Issues X-42 → X-49. Toute avancée théorique met à jour l'issue correspondante.
