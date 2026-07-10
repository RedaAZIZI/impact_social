# Mémo du juge — annotation F3 (aide de lecture, à lire AVEC le guide)

**Statut de ce document.** Ce mémo n'ajoute AUCUNE règle : il reformule en gestes
concrets ce que `docs/GUIDE_ANNOTATION_F3.md` (GELÉ) prescrit. **En cas de doute ou
de conflit apparent, le guide fait foi.** Un cas que ni le guide ni ce mémo ne
tranchent : annote quand même + note en colonne commentaire — jamais d'improvisation
de règle, c'est l'adjudication qui tranchera.

## Ta mission en 5 points

1. Tu annotes **seul** : aucune concertation avec l'autre juge, aucun outil d'IA,
   personne. C'est la condition de validité de toute la mesure.
2. Tu es **en aveugle** : tu ne connais ni l'origine des clauses ni ce qu'une machine
   en a dit — et tu ne cherches pas à le savoir (ne pas ouvrir `sample_key.csv`).
3. Tu traites les clauses **dans l'ordre**, toutes (~2-3 h, fractionnables).
4. Tu ne modifies jamais les colonnes `id` et `clause` ; tu ne supprimes aucune ligne
   (clause illisible → OTHER + commentaire).
5. Avant de commencer : lire le guide EN ENTIER (cas limites §4 compris), puis faire
   les 20 exemples d'entraînement en annexe et te corriger.

## LA règle d'or : pointer le mot

**Une étiquette n'est valide que si tu peux souligner le ou les mots qui la
déclenchent.** Tu n'annotes pas le sens profond de la phrase, ni ce que le contexte
permettrait d'inférer (« quel chien ? quelle plage ? ») — tu annotes les marqueurs
présents en surface. Pas de mot déclencheur → pas d'étiquette.

## Les 4 pointages, dans l'ordre

| # | Cherche… | Étiquette | Exemples de déclencheurs |
|---|---|---|---|
| 1 | un **chiffre** avec unité, monnaie, %, date, heure, âge, température | **A** | « $1.2 billion », « en 2019 », « 8h30 », « 20 years old », « 100 degrees » |
| 2 | un **chiffre** devant un **nom comptable** (on compte, sans instrument) | **N** | « two men », « trois pommes », « une demi-pomme » |
| 3 | un **mot de relation** de la liste fermée | **I** | plus/moins…que, aussi…que, le plus, premier/dernier, avant/après/pendant/jusqu'à (until/before/then), au-dessus/au-dessous, même/égal/différent/opposé, « est un » (is a), implique / « ne veut pas dire » (doesn't mean/imply), tous/aucun/chaque/les deux/la moitié/la majorité (most) |
| 4 | un **mot flou** de la liste fermée | **C** | graduable en forme nue : grand, petit, cher, chaud, vieux, plein, sec… ; beaucoup/peu/plusieurs (many/few) ; environ/presque/« comme »/« ressemble à » (about/almost/like) ; hier/aujourd'hui/récemment |

## Règles de combinaison — les 3 phrases à retenir

- **Plusieurs pointages → plusieurs étiquettes**, en majuscules, séparées par des
  virgules : `I,C`. Balaye TOUTE la clause avant de conclure.
- **OTHER = aucun pointage. OTHER ne se combine JAMAIS avec une autre étiquette.**
  Si tu as pointé quelque chose, OTHER est interdit ; si tu n'as rien pointé,
  OTHER est seul. (Feuille à cases : rien coché = OTHER.)
- **Un doute n'empêche pas d'annoter** : choisis, et note le doute en commentaire.

## Les pièges déjà tranchés (guide §4 — formulation inchangée)

- "standing on **one foot**" → **N** (partie du corps) ; "six **feet** tall",
  "three **feet** of snow" → **A** (unité de mesure).
- "cook **until golden**" → **I,C** (ordre + standard contextuel) — double étiquette
  légitime.
- « **hier** » → **C** (déictique) ; « **en 1998** » → **A** (date chiffrée).
- "**most**/la majorité" → **I** (proportion exacte > ½) ; "**many**/beaucoup" → **C**.
- "**$5 million**" → **A** ; "**5 million people**" → **N** (le multiplicateur suit
  le nom qu'il quantifie).
- "**hot dog**", "high heels", « grand magasin » → composé lexicalisé, PAS **C**.
- "**doesn't mean**/n'implique pas" → **I** (la négation d'une implication reste une
  implication pointée).
- « **comme** / ressemble à » → **C** ; « **le même que** » → **I**.
- « **une dizaine** » → **C** (approximatif) ; « **dix** » → **N**.
- « 1/2 » sans 3e composante = fraction (N ou A selon l'unité qui suit), jamais une
  date.

---

## Annexe — 20 exemples d'entraînement (fais-les AVANT de commencer, puis corrige-toi)

| # | Clause | Réponse | Mot(s) pointé(s) |
|---|---|---|---|
| 1 | Le train part à 8h30. | A | 8h30 (heure) |
| 2 | Quatre chiens courent sur la plage. | N | quatre + chiens |
| 3 | Ce sac est plus lourd que le mien. | I | plus lourd que |
| 4 | L'eau est froide. | C | froide (graduable nu) |
| 5 | Le loyer coûte 950 € par mois. | A | 950 € |
| 6 | Un marteau est un outil. | I | est un |
| 7 | Il y avait peu de monde au marché. | C | peu de |
| 8 | Chaque élève a rendu sa copie. | I | chaque (quantificateur exact) |
| 9 | Elle est née en 1998. | A | en 1998 (date) |
| 10 | Il a couru presque aussi vite que d'habitude. | I,C | aussi…que (équatif) ; presque |
| 11 | Une femme lit un journal. | OTHER | aucun pointage |
| 12 | La moitié des invités sont partis avant le dessert. | I | la moitié ; avant (deux pointages, même classe) |
| 13 | Ajoute 200 g de sucre. | A | 200 g |
| 14 | Ce film ressemble au précédent. | C | ressemble au |
| 15 | He is standing on one foot. | N | one foot (partie du corps, pas unité) |
| 16 | Cook until the onions are golden. | I,C | until ; golden |
| 17 | La réunion a eu lieu hier. | C | hier (déictique, pas une date chiffrée) |
| 18 | The company raised $5 million. | A | $5 million |
| 18b | 5 million people watched the game. | N | 5 million + people |
| 19 | She bought hot dogs for the party. | OTHER | hot dog = composé figé, pas C |
| 20 | Être vieux ne veut pas dire avoir plus de 60 ans. | I,A | ne veut pas dire ; 60 ans (âge chiffré) — « vieux » ici est le sujet dont on parle, mais il reste un graduable nu : I,A,C acceptée aussi, à consigner en commentaire |
