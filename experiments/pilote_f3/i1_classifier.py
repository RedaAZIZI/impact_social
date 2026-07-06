# -*- coding: utf-8 -*-
"""
Pilote F3 — classifieur déterministe de clauses selon la grammaire I1 v0.2.

Classes (multi-étiquettes au niveau phrase) :
  I : fragment invariant EXPLICITE — comparatifs, superlatifs, équatifs, ordre
      temporel/spatial vertical, entre-deux, identité/différence, inclusion
      taxonomique, implication, quantificateurs logiques exacts, rangs.
  C : calibré par le contexte — adjectifs graduables en forme positive (standard
      contextuel θ(κ)), quantités vagues (many/few), approximation/similarité
      (resolution ε_κ), déictiques temporels.
  A : constante d'axe (sortie du fragment) — valeur numérique sur un axe de
      qualité ordonné : monnaie, pourcentage, date, mesure avec unité, âge.
  N : cardinalité — numéral comptant des OBJETS (G n'agit pas sur les comptes :
      invariant). Découverte de la relecture v0.2 : les numéraux bifurquent.
  OTHER : aucun marqueur (prédication catégorielle nue, etc.)

Tout est en règles + listes fermées : le classifieur EST la grammaire, pas un
modèle à valider séparément.
"""
import re

# ---------------------------------------------------------------- lexiques --
UNITS = set("""year years yr yrs month months week weeks day days hour hours hr
hrs minute minutes min mins second seconds sec secs percent percentage pct
dollar dollars cent cents euro euros pound pounds meter meters metre metres km
kilometer kilometers kilometre kilometres mile miles foot feet ft inch inches
yard yards cm mm kg kilogram kilograms gram grams lb lbs ounce ounces oz ton
tons tonne tonnes liter liters litre litres gallon gallons mph kmh degree
degrees acre acres barrel barrels watt watts volt volts calorie calories
decade decades century centuries""".split())

NUMWORDS = set("""one two three four five six seven eight nine ten eleven twelve
thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty
forty fifty sixty seventy eighty ninety hundred thousand million billion
trillion dozen""".split())

MONTHS = set("""january february march april may june july august september
october november december jan feb mar apr jun jul aug sep sept oct nov dec""".split())

COMPARATIVES = set("""bigger smaller larger older younger taller shorter longer
higher lower faster slower stronger weaker heavier lighter earlier later better
worse greater lesser cheaper richer poorer deeper shallower wider narrower
thicker thinner warmer colder hotter cooler harder softer easier tougher safer
closer nearer farther further louder quieter brighter darker newer happier
sadder angrier busier fewer smarter""".split()) | {"more", "less"}

SUPERLATIVES = set("""biggest smallest largest oldest youngest tallest shortest
longest highest lowest fastest slowest strongest weakest heaviest lightest
earliest latest best worst greatest cheapest richest poorest deepest widest
narrowest thickest thinnest warmest coldest hottest coolest hardest softest
easiest safest closest nearest loudest quietest brightest darkest newest
happiest busiest most least fewest first last""".split())

ORDER_TEMPORAL = set("""before after during until till then previous prior
following next earlier later meanwhile precedes preceded follows followed
between above below beneath simultaneously""".split())

IDENTITY = set("""same equal equals identical different differs differ opposite
unequal""".split())

QUANT_LOGIC = set("""all every each none nobody nothing everyone everybody
noone both neither majority half whole entire""".split())

GRADABLE = set("""big large small little tall short long wide narrow thick thin
deep shallow high low heavy light fast quick slow old young new recent early
late hot cold warm cool expensive cheap rich poor strong weak hard soft tough
easy difficult loud quiet noisy bright dark clean dirty wet dry full empty open
closed straight crowded busy calm dangerous safe risky common rare popular
famous important serious severe huge tiny enormous massive giant vast major
minor good bad great terrible awful nice beautiful pretty ugly handsome smart
intelligent stupid dumb crazy weird strange normal typical unusual happy sad
angry mad upset tired hungry thirsty sick healthy fit fat skinny slim frequent
significant substantial considerable extreme moderate steep sharp gentle rough
smooth simple complex plain fancy modern ancient fresh stale wealthy broke
crowded packed sparse dense scarce abundant plentiful""".split())

KENNEDY_ABSOLUTE = set("""full empty open closed straight dry wet clean pure
complete flat""".split())  # standards d'extrémité (Kennedy 2007) — lien L3

VAGUE_QUANT = set("""many few several numerous lots plenty countless""".split())

APPROX = set("""about around approximately nearly almost roughly similar alike
resembles resemble""".split())

DEICTIC_TIME = set("""today yesterday tomorrow now currently recently
nowadays""".split())

INTENSIFIERS = set("""very really extremely quite too so incredibly super
fairly rather pretty remarkably""".split())

CAT_NOUNS_GROUP = set("""group crowd lot amount number bunch handful couple
majority minority portion fraction share""".split())

RE_MONEY = re.compile(r"[$€£]\s*\d")
RE_PCT = re.compile(r"\d\s*(?:%|percent\b|percentage point)")
RE_YEAR = re.compile(r"\b(1[89]\d\d|20[0-3]\d)\b")
RE_DATE_SLASH = re.compile(r"\b\d{1,2}/\d{1,2}(/\d{2,4})?\b")
RE_TIME = re.compile(r"\b\d{1,2}(:\d{2})?\s*(a\.?m\.?|p\.?m\.?|o'?clock)\b", re.I)
RE_NUM = re.compile(r"\d+(?:[.,]\d+)?")
RE_ER_THAN = re.compile(r"\b(\w{3,}er)\s+than\b")
RE_AS_AS = re.compile(r"\bas\s+\w+\s+as\b")
RE_YEAR_OLD = re.compile(r"\b\d+[- ]?years?[- ]old\b")
RE_ORDINAL = re.compile(r"\b(\d+)(st|nd|rd|th)\b")
RE_TAXO = re.compile(r"\b(is|are|was|were)\s+(a|an)\b")
RE_KINDOF = re.compile(r"\b(type|kind|form|sort|example|part|piece|member)s?\s+of\b")
RE_IMPLY = re.compile(r"\b(means?|meant|impl(?:y|ies|ied)|refers? to|synonym|"
                      r"necessarily|entails?|infer(?:s|red)?)\b")
RE_JUSTBC = re.compile(r"\bjust because\b|\bdoes\s?n[o']t (mean|imply|make)\b|"
                       r"\bcan\s?not\b.*\bat the same time\b")
RE_THAN = re.compile(r"\bthan\b")
RE_EXCL_THAN = re.compile(r"\b(rather|other)\s+than\b")
RE_LOOKLIKE = re.compile(r"\blooks?\s+like\b|\bclose\s+to\b")

TOKEN = re.compile(r"[a-zA-Z']+|\d+(?:[.,]\d+)?|[%$€£]")


def tokenize(s):
    return TOKEN.findall(s.lower())


def classify(sentence):
    """Retourne dict de booléens {A, N, I, C} + sous-marqueurs + calib_shaped."""
    s = sentence.strip()
    low = " " + s.lower() + " "
    toks = tokenize(s)
    tags = {"A": False, "N": False, "I": False, "C": False}
    sub = set()

    # ---------------- A : constantes d'axe ----------------
    if RE_MONEY.search(s):
        tags["A"] = True; sub.add("A:money")
    if RE_PCT.search(low):
        tags["A"] = True; sub.add("A:percent")
    if RE_YEAR.search(s) or RE_DATE_SLASH.search(s) or RE_TIME.search(s):
        tags["A"] = True; sub.add("A:date")
    if RE_YEAR_OLD.search(low):
        tags["A"] = True; sub.add("A:age")
    # mois + numéral adjacent -> date
    for i, t in enumerate(toks):
        if t in MONTHS and any(RE_NUM.fullmatch(x) for x in toks[max(0, i-2):i+3]):
            tags["A"] = True; sub.add("A:date")
    # numéral suivi (à <=2 tokens) d'une unité -> mesure
    for i, t in enumerate(toks):
        if RE_NUM.fullmatch(t) or t in NUMWORDS:
            window = toks[i+1:i+3]
            for j, w in enumerate(window):
                if w in UNITS:
                    if w in ("foot", "feet"):
                        nxt = toks[i+2+j] if i+2+j < len(toks) else ""
                        if nxt not in ("of", "tall", "deep", "high", "long",
                                       "wide", "away", "above", "below"):
                            continue  # partie du corps, pas une unité
                    tags["A"] = True; sub.add("A:measure")

    # ---------------- N : cardinalités (comptes d'objets) ----------------
    for i, t in enumerate(toks):
        isnum = bool(RE_NUM.fullmatch(t)) or (t in NUMWORDS and t != "one")
        if t == "one" and i + 1 < len(toks) and toks[i+1] not in ("of", "who",
                                                                 "that", "in"):
            isnum = True
        if isnum:
            window = toks[i+1:i+3]
            if window and not any(w in UNITS for w in window) \
               and not any(w in MONTHS for w in window):
                # numéral non consommé par une unité -> compte d'objets
                if not (RE_MONEY.search(s) and i < 3):
                    tags["N"] = True; sub.add("N:count")

    # ---------------- I : fragment invariant explicite ----------------
    if (RE_THAN.search(low) and not RE_EXCL_THAN.search(low)) \
       or RE_ER_THAN.search(low):
        tags["I"] = True; sub.add("I:comparatif")
    if any(t in COMPARATIVES for t in toks):
        tags["I"] = True; sub.add("I:comparatif")
    if any(t in SUPERLATIVES for t in toks):
        tags["I"] = True; sub.add("I:superlatif")
    if RE_AS_AS.search(low):
        tags["I"] = True; sub.add("I:equatif")
    if any(t in ORDER_TEMPORAL for t in toks):
        tags["I"] = True; sub.add("I:ordre")
    if any(t in IDENTITY for t in toks):
        tags["I"] = True; sub.add("I:identite")
    if RE_TAXO.search(low) or RE_KINDOF.search(low):
        tags["I"] = True; sub.add("I:taxonomie")
    if RE_IMPLY.search(low) or RE_JUSTBC.search(low):
        tags["I"] = True; sub.add("I:implication")
    if any(t in QUANT_LOGIC for t in toks):
        tags["I"] = True; sub.add("I:quantif")
    m = RE_ORDINAL.search(low)
    if m and any(t in SUPERLATIVES for t in toks):
        tags["I"] = True; sub.add("I:rang")

    # ---------------- C : calibré par le contexte ----------------
    for i, t in enumerate(toks):
        if t in GRADABLE:
            prev = toks[i-1] if i > 0 else ""
            if prev not in ("more", "less", "as", "most", "least"):
                tags["C"] = True
                sub.add("C:graduable-absolu" if t in KENNEDY_ABSOLUTE
                        else "C:graduable")
                if prev in INTENSIFIERS:
                    sub.add("C:intensifie")
    if any(t in VAGUE_QUANT for t in toks):
        tags["C"] = True; sub.add("C:quantite-vague")
    if any(t in APPROX for t in toks) or RE_LOOKLIKE.search(low):
        tags["C"] = True; sub.add("C:approx")
    if any(t in DEICTIC_TIME for t in toks):
        tags["C"] = True; sub.add("C:deixis")

    # ------------- forme « calibration » : NUM <-> concept graduable -------
    has_num = any(RE_NUM.fullmatch(t) or t in NUMWORDS for t in toks)
    has_grad_or_group = any(t in GRADABLE or t in CAT_NOUNS_GROUP for t in toks)
    has_cop = re.search(r"\b(is|are|was|were|makes?|counts?|considered)\b", low)
    calib = bool(has_num and has_grad_or_group and has_cop)

    # classe exclusive (priorité A > I > C > N > OTHER) pour la composition
    if tags["A"]:
        excl = "A"
    elif tags["I"]:
        excl = "I"
    elif tags["C"]:
        excl = "C"
    elif tags["N"]:
        excl = "N"
    else:
        excl = "OTHER"
    return {"tags": tags, "sub": sorted(sub), "excl": excl,
            "calib_shaped": calib}


if __name__ == "__main__":
    tests = [
        "A dog is an animal.",
        "Just because a man is sitting does not mean he is waiting.",
        "The older man is taller than the boy.",
        "Two men are playing guitar.",
        "The unemployment rate was 9.5 percent in 2010.",
        "He spent $1.2 million on the campaign.",
        "A group of 13 people is a large group.",
        "The woman is very tall.",
        "The glass is full.",
    ]
    for t in tests:
        r = classify(t)
        print(f"{r['excl']:6s} {r['sub']} calib={r['calib_shaped']}  | {t}")
