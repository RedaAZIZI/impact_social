# Papier — preprint arXiv

Cible : position paper 6-8 pages, cs.LG (cross-list cs.AI), à partir de `docs/article_source_explicabilite.md`.

## Sources

- `main.tex` — le preprint (anglais). Titre acté (décision D1) : *Explainability is Relational: A Receiver-Dependent Framework for AI Interpretability*.
- `references.bib` — les références de la section 4.5 du document source (années et auteurs à re-vérifier une à une : issue S-58).
- `figures/` — les 4 figures du papier (copies de `/figures` pour une soumission autonome) : exp1_courbes, exp2_dialogue, exp6_ai4i, exp7_living_graph.
- `main.pdf` — le PDF compilé, commité pour la relecture.

## Compilation

```bash
latexmk -pdf main.tex
```

(TeX Live avec `texlive-latex-recommended`, `texlive-latex-extra`, `texlive-fonts-recommended`, `texlive-bibtex-extra`.)

## Consignes de rédaction (section 13 du document source — font foi)

- La vision et l'approche sont posées par l'auteur (Reda) ; ne pas les altérer, les mettre en forme.
- Ton : ambitieux sur le cadre, sobre sur les preuves. Chaque claim empirique pointe vers les tableaux du document source.
- Ne pas sur-vendre : pas de claim sur les humains ; les claims sur données réelles se limitent aux tableaux des sections 10-12.
- L'apprentissage par édition se formule en conjecture assumée, jamais en claim établi.

## Avant soumission (bloquants)

1. **Abstract étendu** : la version dans `main.tex` implémente la proposition de la section 16 du document source — **à valider par Reda avant toute publication**.
2. **Figures en français** : les 4 figures ont titres et axes en français. À régénérer en anglais — exp1/exp2/exp7 sont synthétiques (relance locale, seeds fixées), exp6 exige le fichier AI4I déposé par Reda (réseau sortant restreint).
3. **Biblio** : vérification finale entrée par entrée (S-58).
4. Relecture Reda, puis dépôt arXiv par Reda (S-59, checklist dans l'issue).
