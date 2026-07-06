# Programme Exp 8 — Distiller un LLM en un gros graphe qui vit

**Statut : DESIGN v2 — aucun appel API tant que Reda n'a pas donné le go palier par palier.**
Pré-enregistrement du programme : Linear X-29. Budget plafond utilisateur : 100 €, engagé progressivement.
v2 (2026-07-06) intègre deux remarques de Reda : (1) domaine **informel** plutôt que le crédit
(« arbre de décision par construction » → quasi circulaire) ; (2) spécification complète du
**protocole W sur un LLM** (comment le modèle décide, comment il répond à « pourquoi », et
comment nos concepts en sortent).

## Grand objectif

Démontrer la vision §3.3 de l'article sur un modèle frontière réel : un LLM (Claude Haiku)
peut être **distillé en un graphe de décision explicable** — pas un jouet de 32 feuilles,
un **gros** graphe — et ce graphe peut **vivre** : être interrogé (W), corrigé en une phrase
(W⁻¹), étendu par accrétion de contextes, et maintenu **sans jamais régresser hors de la
région éditée** (localité par construction).

Le passage au domaine informel élève la mise : si le jugement *informel* d'un LLM — là où
aucune procédure de décision n'existe par construction — se distille en un graphe fidèle,
on a montré une structure latente là où personne ne l'a écrite. Et si la courbe plafonne
bas, on a **mesuré le désalignement entre la base d'un LLM et un vocabulaire de concepts
humains** — l'Exp 1 sur un modèle frontière. Les deux issues sont des résultats.

---

## 1. Le domaine : jugement social informel (décision Reda, remarque 1)

**Tâche de M** : juger des situations sociales quotidiennes racontées en langage naturel.
Exemple de vignette : « Ton collègue proche, qui avait promis d'être là, arrive 25 minutes
en retard à ta soutenance. Il s'excuse brièvement en riant. C'est la deuxième fois. »
**Réponse demandée** : un label parmi {acceptable, maladroit, inacceptable} — jugement
ordinal à 3 classes, informel par nature : il n'existe AUCUN arbre de décision canonique
pour ça.

**Facteurs latents contrôlés** (~6, tirés aléatoirement, réalisés en texte par gabarits) :
gravité du dommage, intentionnalité apparente, proximité relationnelle, répétition,
présence/qualité d'excuse, contexte public ou privé.

**Les trois vocabulaires du récepteur** :
- **Brut** : les 6 facteurs latents tels quels.
- **Expert (mélange)** : brut + concepts composés de psychologie morale —
  *culpabilité* = gravité × intentionnalité (théorie de l'attribution),
  *trahison* = proximité × promesse non tenue,
  *réparation* = qualité d'excuse × (1 − répétition).
- **Contrôle monotone** : déformations coordonnée-par-coordonnée (inerte prédit, Prop 1).

**Réalisation textuelle** : gabarits déterministes d'abord (le texte est une fonction des
facteurs) ; la robustesse aux paraphrases est un stress test ultérieur, pas une variable
confondante du run principal.

**Contexte d'accrétion pour le palier 5** : d'autres domaines informels — modération d'un
chat d'équipe (« ce message est-il ok ici ? »), conseil cadeau, arbitrage de conflit léger.
Hétérogènes entre eux mais partageant des facteurs (gravité, intention, proximité) : c'est
le test dur de l'assemblage de sous-graphes et de la localité inter-contextes.

## 2. Le protocole W sur un LLM (décision Reda, remarque 2)

### 2.1 Comment M décide (le comportement)

- Un appel API = une vignette. Prompt système figé, temperature 0, réponse = **le label
  seul** (pas de chaîne de raisonnement demandée). C'est la face comportementale de M :
  ce que M *fait*, mesuré proprement, sans que l'acte d'expliquer contamine l'acte de juger.
- Variante optionnelle (coût en plus, non pré-enregistrée) : condition « raisonne
  brièvement puis réponds » — le graphe distillé change-t-il quand M pense tout haut ?

### 2.2 Comment M répond à « pourquoi » (l'introspection) — trois canaux, du plus contraint au plus libre

- **W-fermé** : « Quels facteurs ont pesé dans ton jugement ? Choisis-en 2-3, par ordre
  d'importance, uniquement dans cette liste : [étiquettes du vocabulaire, facteurs bruts
  ET concepts composés]. » → directement parsable, c'est l'exigence de *traduisibilité*
  de W (réponse dans le vocabulaire du récepteur).
- **W-contrastif** : « Pourquoi "inacceptable" plutôt que "maladroit" ? » → la réponse
  attendue = les facteurs pivots ; on mesure la taille et l'asymétrie des réponses
  contrastives comme dans l'Exp 4, mais sur un vrai LLM.
- **W-libre** : « Pourquoi ? » ouvert → texte libre, codé ensuite dans le vocabulaire par
  correspondance lexicale déterministe (pas de LLM-codeur : circularité), avec
  vérification manuelle d'un échantillon.

**Séparation causale** : le « pourquoi » est TOUJOURS un appel séparé, postérieur à la
décision, recevant la vignette + le label déjà rendu. L'explication ne peut donc pas
influencer la décision — on teste bien l'introspection *post hoc*, ce que la psychanalyse
du palier 3 exige.

### 2.3 Comment nos concepts sortent (la table de correspondance)

| Concept REX | Réalisation dans l'Exp 8 |
|---|---|
| M | Haiku + prompt système + contexte, figés (temp 0, version snapshotée) |
| V_R (base du récepteur) | les 3 vocabulaires (brut / expert-mélange / contrôle monotone) |
| Expl(M, R, ε), courbe | distillation du comportement en graphes de budget croissant, fidélité équilibrée |
| **W révélé** | `extract_rule` : le chemin qui décide x dans le graphe distillé |
| **W déclaré** | les 3 canaux d'introspection (fermé / contrastif / libre) |
| Fidélité introspective | recouvrement déclaré/révélé, par cas et en agrégat (corrélation de rangs) |
| Q contrastive (Exp 4) | canal W-contrastif : taille et asymétrie des réponses par paire de labels |
| W⁻¹ | édition du graphe local ; comparée au re-prompt de M (palier 4) |

---

## 3. Les paliers

Chaque palier = une hypothèse + un critère de falsification écrits AVANT le run + un budget.
On ne passe au suivant que si le précédent survit. Réponses en cache disque et **snapshotées
dans le repo** (le comportement d'un modèle hébergé change avec les versions). Garde-fou
`--max-calls`, coût imprimé à chaque run. Modèle : `claude-haiku-4-5`.

### Palier 0 — Plomberie (0 €, sans API)
Mock : un « juge social » à règle cachée écrite dans les concepts composés (culpabilité,
trahison) + bruit 2 %. **Sortie** : le pipeline vignette → label → graphe → courbes →
édition retrouve la règle cachée (fidélité > 0.95, dominance experte détectée, localité
vérifiée), les 3 canaux W tournent en mock.

### Palier 1 — La photographie (~1-2 €) — go/no-go technique
N ≈ 1000 vignettes. **Question** : le jugement social de Haiku est-il assez cohérent pour
être distillé ? **Mesures** : auto-accord sur re-requêtes ; plafond de fidélité (64
feuilles) ; taux de classe majoritaire. **Kill** : auto-accord < 95 % ou plafond <
majorité + 10 pts → resserrer le contexte avant toute suite. Domaine informel = risque
de kill plus élevé qu'au crédit : assumé, c'est précisément ce qu'on veut savoir.

### Palier 2 — La courbe d'explicabilité d'un LLM (~5-10 €)
N ≈ 5000. **H8a** : le jugement social de Haiku vit dans les concepts composés → le
vocabulaire expert domine (arc GBT → MLP → LLM). **Falsification** : écart < 1 std.
**Lecture supplémentaire propre au domaine informel** : le niveau absolu du plateau mesure
la part du jugement de Haiku qui est *exprimable* dans un vocabulaire humain de facteurs —
désalignement naturel LLM↔humain, chiffré.

### Palier 3 — Psychanalyse (~2-3 €)
~30 cas de bord × 3 canaux W. **H8b** : recouvrement majoritaire déclaré/révélé sur le
canal fermé ; l'asymétrie contrastive (canal 2) reproduit qualitativement l'Exp 4.
**Bidirectionnel** : accord → l'introspection est validée par la structure ; désaccord →
infidélité des auto-explications quantifiée par le graphe comportemental. Publiable dans
les deux sens.

### Palier 4 — La boucle fermée (~5-10 €)
La norme sociale change en UNE phrase (« désormais, un retard non excusé à un événement
important est inacceptable, même venant d'un proche »). Voie A : édition du graphe (0
appel, locale par construction). Voie B : re-prompt de Haiku avec la norme amendée.
**H8c** : graphe édité = 100 % conforme en région cible + zéro dérive hors cible ; Haiku
re-prompté = conforme mais dérive hors cible. Si confirmé : **le graphe se corrige plus
proprement que le LLM lui-même.**

### Palier 5 — Le GROS graphe (~10-30 €) — le livrable-titre
Accrétion de contextes informels (jugement social → modération de chat → conseil →
arbitrage), sous-graphes partageant les facteurs communs. **Questions d'échelle** :
fidélité quand |G| ×10 ; localité inter-contextes exacte ; W(x) reste un petit chemin
(*le graphe grossit, l'explication ne grossit pas*) ; cohérence après des dizaines
d'éditions (règles mortes, conflits, couverture).

### Palier 6 — Perspectives (hors budget)
Changelog comportemental entre versions du modèle (re-distiller, diff-er les graphes) ;
graphe personnel qui grandit avec l'utilisateur ; comparaison des structures Haiku vs
Sonnet ; robustesse aux paraphrases.

---

## Discipline

- Aucun appel API sans go explicite de Reda sur le palier concerné (commentaire GO sur l'issue).
- Plafond cumulé 100 € ; `--max-calls` ; coût imprimé ; snapshots commités ; vignettes
  synthétiques uniquement, zéro donnée personnelle.
- Invariants hérités des Exp 5-7 : fidélité équilibrée, vérification de la structure de M
  avant interprétation, contrôle monotone systématique, pré-enregistrement.
