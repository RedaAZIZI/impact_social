# Papier — preprint arXiv

Cible : position paper 6-8 pages, cs.LG (cross-list cs.AI), à partir de `docs/article_source_explicabilite.md`.

## Sources

- `main.tex` — le preprint (anglais). Titre acté (décision D1) : *Explainability is Relational: A Receiver-Dependent Framework for AI Interpretability*.
- `references.bib` — les références de la section 4.5 du document source (années et auteurs à re-vérifier une à une : issue S-58).
- `figures/` — les figures du papier (copies de `/figures` pour une soumission autonome) : exp1_courbes, exp2_dialogue, exp7_living_graph (anglais, régénérées de zéro, chiffres vérifiés identiques).
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
2. **Figure exp6 retirée du papier** (elle était en français ; le Tableau 4 porte l'intégralité du résultat avec les stats appariées). Pour la réintégrer en anglais : Reda dépose `data/ai4i2020.csv` (UCI bloqué depuis l'environnement), puis `exp6_predictive_maintenance.py --seeds 10` (et `--model gbt`) — le script trace désormais en anglais — et remettre le bloc figure dans `main.tex` (section Experiment 6).
3. **Biblio** : vérification finale entrée par entrée (S-58).
4. Relecture Reda, puis dépôt arXiv par Reda (S-59, checklist dans l'issue).
