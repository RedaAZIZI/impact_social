# Programme Exp 8 — Distiller un LLM en un gros graphe qui vit

**Statut : DESIGN — aucun appel API tant que Reda n'a pas donné le go palier par palier.**
Pré-enregistrement du programme : Linear X-29. Budget plafond utilisateur : 100 € (clé API), engagé progressivement.

## Grand objectif

Démontrer la vision §3.3 de l'article sur un modèle frontière réel : un LLM (Claude Haiku)
peut être **distillé en un graphe de décision explicable** — pas un jouet de 32 feuilles,
un **gros** graphe — et ce graphe peut **vivre** : être interrogé (W), corrigé en une phrase
(W⁻¹), étendu par accrétion de contextes, et maintenu dans le temps **sans jamais régresser
hors de la région éditée** (localité par construction, testée par `/tests/test_edit.py`).

Si le programme aboutit, on a l'objet que le papier appelle « compression contextuelle » et
que le produit appelle « edge AI corrigeable » : un artefact local, frugal, entièrement
explicable, adossé à un LLM mais capable d'évoluer sans lui.

## Le fil qui relie les paliers

Chaque palier réutilise le moteur existant (`core/rex`, `LivingGraph` de l'Exp 7,
fidélité équilibrée de l'Exp 6) et répond à UNE question falsifiable. On ne passe au
palier suivant que si le précédent survit. Les réponses du LLM sont mises en cache sur
disque et **snapshotées dans le repo** (le comportement d'un modèle hébergé change avec
les versions — le snapshot est la condition de reproductibilité). Temp 0, garde-fou
`--max-calls`, coût imprimé à chaque run.

---

## Palier 0 — Plomberie (0 €, sans API) — prêt à coder

Monde : demandes de crédit en langage naturel, générées depuis des features structurées
(âge, revenu, montant, durée, ancienneté, autres crédits). Une « banque mock » à règle
cachée écrite en concepts experts (taux d'effort = mensualité/revenu) joue le rôle du LLM.
**Question** : la chaîne vignette → décision → distillation → courbes → édition tourne-t-elle
de bout en bout ? **Critère** : le pipeline retrouve la règle cachée du mock (fidélité > 0.95,
dominance du vocabulaire expert détectée). Identique en esprit aux dry-runs des Exp 5-6.

## Palier 1 — La photographie (~1-2 €)

N ≈ 1000 vignettes, Haiku analyste crédit avec une politique volontairement vague (pour que
SA structure de jugement émerge, pas une règle récitée).
**Question (go/no-go technique du programme)** : le comportement de Haiku-dans-ce-contexte
est-il assez cohérent pour être distillé ?
**Mesures** : auto-accord sur re-requêtes identiques ; plafond de fidélité d'un graphe 64
feuilles ; taux de classe majoritaire (leçon Exp 5 : vérifier qu'il y a de la structure).
**Kill** : auto-accord < 95 % ou fidélité plafond < majorité + 10 pts → le contexte doit être
resserré avant toute suite.

## Palier 2 — La courbe d'explicabilité d'un LLM (~5-10 €)

N ≈ 5000. Courbes de fidélité équilibrée dans trois vocabulaires (brut, expert-mélange,
contrôle monotone).
**Hypothèse H8a** : un LLM raisonne sémantiquement en concepts composés → le vocabulaire
expert domine, contrairement au GBT de l'Exp 6. Complète l'arc « base interne de M » :
GBT (axis-aligned) → écart nul ; MLP → +0.045 ; LLM → écart prédit maximal.
**Falsification** : écart < 1 std ⇒ le LLM se comporte comme un modèle axis-aligned — ce qui
serait en soi un résultat surprenant et publiable.
À notre connaissance, personne n'a publié la courbe d'explicabilité d'un LLM ; à vérifier
en biblio avant rédaction.

## Palier 3 — Psychanalyse de l'IA (~2-3 €)

Sur ~30 cas de bord : demander à Haiku « pourquoi ? » (W déclaré, facteurs à choisir dans
une liste fermée) et comparer aux prédicats que le graphe distillé révèle (W révélé).
**Hypothèse H8b** : recouvrement majoritaire déclaré/révélé.
**Intérêt bidirectionnel** : si ça recoupe, l'introspection de Haiku est honnête et le graphe
la valide ; si ça ne recoupe pas, on a **quantifié l'infidélité des auto-explications d'un
LLM par son graphe comportemental** — publiable dans les deux sens. C'est la psychanalyse :
ce que le patient dit de lui vs ce que sa structure révèle.

## Palier 4 — Le graphe adossé au LLM qui vit (~5-10 €)

La boucle de l'Exp 7, mais M = Haiku. La politique change en UNE phrase (« désormais,
refuser si durée > 60 mois »).
- **Voie A** : édition du graphe distillé (0 appel API, milliseconde, locale par construction).
- **Voie B** : re-prompt de Haiku avec la politique amendée (coût par décision pour toujours).
**Hypothèse H8c** : le graphe édité est 100 % conforme dans la région cible et **zéro dérive
hors cible** (garanti par construction) ; Haiku re-prompté est conforme mais **dérive hors
cible** (effets de bord non locaux du prompt — la fragilité documentée des LLM).
Si confirmé : **le graphe distillé se corrige plus proprement que le LLM lui-même** — et il
tourne sans réseau, sans API, sans latence. La thèse produit, démontrée sur modèle frontière.

## Palier 5 — Le GROS graphe (~10-30 €) — là où « vivre » prend son sens

Passage à l'échelle par **accrétion de contextes** : crédit conso, puis immo, puis pro,
puis assurance... Chaque contexte est distillé à la demande en un sous-graphe (compression
contextuelle) ; les sous-graphes partagent le vocabulaire et s'assemblent en un graphe de
centaines puis milliers de règles.
**Questions d'échelle** (chacune falsifiable) :
1. **Fidélité** : tient-elle quand |G| croît d'un ordre de grandeur ?
2. **Localité à l'échelle** : une édition dans le contexte k laisse-t-elle les k−1 autres
   exactement intacts ? (prédit par construction — à vérifier sur 10³ règles, l'invariant
   de test doit passer tel quel)
3. **Coût d'explication** : W(x) reste-t-il petit (un chemin) même quand le graphe est
   gros ? — c'est la promesse centrale : *le graphe grossit, l'explication ne grossit pas*.
4. **Maintenance** : après des dizaines d'éditions accumulées sur des contextes différents,
   le graphe reste-t-il cohérent (pas de règles mortes/contradictoires) ? Métriques :
   couverture des règles, règles jamais tirées, taux de conflit.

**C'est le livrable-titre du programme** : « un graphe de N·10³ règles, distillé d'un LLM,
qui vit — interrogeable, corrigeable en une phrase, extensible par accrétion, zéro
régression inter-contextes ».

## Palier 6 — Perspectives (hors budget, à ne pas faire maintenant)

- **Changelog comportemental automatique** : re-distiller le même contexte sur une nouvelle
  version du modèle et diff-er les graphes → instrument de mesure des changements de
  comportement entre versions de LLM. Personne n'a cet outil.
- Graphe personnel qui grandit avec son utilisateur (vision c de l'article).
- Comparer les structures distillées de modèles différents (Haiku vs Sonnet) : la base
  interne diffère-t-elle entre tailles de modèles ?

---

## Discipline

- Un palier = une hypothèse + un critère de falsification écrits AVANT le run + un budget.
- Aucun appel API sans go explicite de Reda sur le palier concerné.
- Réponses LLM snapshotées et commitées (reproductibilité) ; jamais de données personnelles
  (vignettes synthétiques uniquement).
- Les leçons des Exp 5-7 sont des invariants du protocole : fidélité équilibrée, vérification
  de la structure de M avant interprétation, contrôle monotone systématique.
