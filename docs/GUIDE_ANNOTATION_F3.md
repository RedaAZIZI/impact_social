> **Provenance** : étude complémentaire externe (2e livraison, 2026-07-06), intégrée
> comme protocole candidat pour le F3 propre (X-48). Guide GELÉ avant annotation
> (esprit A-G18) ; complète `I1_grammaire_fragment_invariant.md` (X-43).

# Guide d'annotation F3 — grammaire I1 v0.2 (quatre classes)

**Usage** : protocole pour juges humains indépendants (≥ 2), en vue du F3 propre.
Ce guide est GELÉ avant le début de l'annotation (esprit A-G18) : tout cas limite
découvert en cours est consigné, tranché en adjudication, et versé à la v
suivante — jamais appliqué rétroactivement à la volée.

## 1. Unité et tâche

L'unité est la **clause** (proposition à un prédicat). Une phrase peut porter
plusieurs clauses ; en cas de doute, découper aux conjonctions et aux relatives.
Chaque clause reçoit un ensemble d'étiquettes (multi-étiquettes autorisées) parmi
**I, C, A, N**, plus OTHER si aucune ne s'applique. Pour les statistiques, la
classe exclusive est obtenue par priorité A > I > C > N > OTHER.

## 2. Les quatre classes — définitions opératoires

**A — constante d'axe.** La clause mentionne une valeur numérique SUR UN AXE DE
QUALITÉ ORDONNÉ : monnaie, pourcentage, date ou heure, mesure avec unité, âge
chiffré, température. Test : la valeur exige-t-elle une échelle pré-calibrée
(unité, calendrier, devise) pour être comprise ? — EN : "the deficit grew by
$1.2 billion in 2009" ; FR : « il mesure 1,85 m », « en 2019 ».

**N — cardinalité.** Numéral comptant des OBJETS (nom comptable), sans unité.
Invariant : le groupe G déforme les axes, pas le nombre d'objets. — EN : "two
men are playing guitar" ; FR : « trois personnes attendent ». Fractions
d'objets (« une demi-pomme ») → N.

**I — fragment invariant explicite.** Comparatifs et équatifs ; superlatifs et
rangs ; ordre temporel ou spatial vertical (avant/après/pendant/jusqu'à,
au-dessus/au-dessous, entre) ; identité/différence qualitative (même, égal,
différent, opposé) ; inclusion taxonomique (« X est un Y », « une sorte de ») ;
implication et son refus (« implique », « ne veut pas dire », « n'entraîne
pas ») ; quantificateurs exacts (tous, aucun, chaque, les deux, la moitié, la
majorité). — EN : "an apple is a fruit", "taller than", "most of them" ;
FR : « plus grand que », « la moitié des invités ».

**C — calibré par le contexte.** Adjectif graduable en FORME POSITIVE, sans
comparatif ni mesure (« grand », « cher ») — le standard vient de la classe de
comparaison ; quantités vagues (beaucoup, peu, plusieurs) ; approximation et
similarité (environ, presque, semblable, « ressemble à ») ; déictiques
temporels (aujourd'hui, hier, récemment). — EN : "the room is large",
"about fifty people" ; FR : « il fait chaud », « à peu près ».

**OTHER.** Prédication catégorielle nue sans marqueur ci-dessus (« un homme
marche ») ; méta-discours ; citations.

## 3. Arbre de décision (à suivre dans l'ordre)

1. La clause contient-elle un numéral ?
   a. suivi/précédé d'une unité, d'un symbole monétaire, d'un % → **A** ;
   b. forme date/heure (année, mois+jour, hh:mm) → **A** ;
   c. suivi d'un nom comptable → **N** ;
   d. ordinal : devant un superlatif (« le 3e plus grand ») → **I** (rang) ;
      dans une date → **A**.
2. Y a-t-il un marqueur relationnel (comparatif, superlatif, équatif, ordre,
   identité, inclusion, implication, quantificateur exact) ? → **I**.
3. Y a-t-il un graduable en forme positive, une quantité vague, une
   approximation, un déictique ? → **C**.
4. Sinon → **OTHER**.
Étapes non exclusives : appliquer 1 puis 2 puis 3 et cumuler les étiquettes.

## 4. Cas limites tranchés (issus des audits du pilote)

- **Parties du corps vs unités** : "standing on one foot" → N (objet), pas A ;
  "three feet of snow", "six feet tall" → A.
- **Fractions vs dates** : « 1/2 » sans troisième composante = fraction (N ou A
  selon l'unité qui suit), jamais une date.
- **Composés lexicalisés** : "high heels", "hot dog", « grand magasin » — le
  graduable figé dans un nom composé ne compte PAS comme C.
- **« until » + graduable** ("cook until golden") → I (ordre) ET C (standard
  contextuel) : double étiquette légitime.
- **most/majority** (proportion exacte > ½) → I ; **many/few/beaucoup/peu**
  (standard vague) → C.
- **Négation d'implication** ("doesn't mean", « ne veut pas dire ») → I au même
  titre que l'implication.
- **Adjectifs absolus de Kennedy** (plein, vide, droit, sec) → C, avec
  sous-étiquette C-abs si le schéma la prévoit (standard d'extrémité, cf.
  PREUVES v0.2, Rem. 4.3).
- **Déictiques** (hier, aujourd'hui) → C (constante indexicale calibrée par la
  situation), PAS A ; une date chiffrée → A.
- **Similarité** (« comme », « ressemble à ») → C ; **identité stricte**
  (« le même que ») → I.
- **Numéraux multiplicateurs** (million, milliard) : suivent la règle du nom
  qu'ils quantifient ("5 million people" → N ; "$5 million" → A).

## 5. Procédure et mesure d'accord

- Échantillon : 200–500 clauses, stratifiées par registre (au moins un registre
  explicatif, un registre de calibration, un intermédiaire).
- ≥ 2 juges annotent en aveugle ; accord mesuré par κ de Cohen (2 juges) ou de
  Fleiss (> 2), par classe et global ; cible κ ≥ 0,7 sur la classe A (verrou de
  F3 : si les clauses réelles sont majoritairement inclassables, [Déf 2.3] n'est
  pas mesurable).
- Désaccords : adjudication à trois, consignée ; le guide n'est amendé qu'entre
  deux campagnes.
- Pré-enregistrer les prédictions (P1, P2a, P2b — RESULTATS_PILOTE_F3.md §1)
  avant d'ouvrir les données.

## 6. Annexe — lexiques squelettes pour le français

- I : plus/moins … que, aussi … que, autant que, le plus/le moins, premier/
  dernier, avant, après, pendant, jusqu'à, puis, ensuite, entre, au-dessus,
  au-dessous, même, égal, différent, opposé, est un(e), une sorte de, implique,
  signifie, veut dire, tous, aucun, chaque, chacun, les deux, la moitié, la
  majorité.
- C : grand, petit, long, court, haut, bas, lourd, léger, rapide, lent, vieux,
  jeune, cher, chaud, froid, riche, pauvre, fort, faible, dur, doux, profond,
  large, étroit, plein, vide, sec, propre, sale, beaucoup, peu, plusieurs,
  environ, presque, à peu près, semblable, comme, hier, aujourd'hui, récemment,
  très, trop, assez.
- A : unités SI et usuelles, €, $, %, années (19xx/20xx), mois + jour, hh:mm,
  °C, ans (âge chiffré).
- N : numéraux + noms comptables ; attention aux partitifs (« une dizaine » → C
  approximatif ; « dix » → N).
