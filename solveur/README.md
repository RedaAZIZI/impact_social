# SOLVEUR — solveur ARC-AGI explicable

## Thèse

Les solveurs ARC-AGI actuels les plus performants sont soit des LLM opaques
(on ne sait pas *pourquoi* la grille produite est la bonne), soit des
recherches de programmes massives dont la sortie n'est pas une explication.
SOLVEUR parie qu'un couple **proposeur/vérifieur** fait mieux que chacun
seul : un LLM propose des hypothèses de transformation, un vérifieur
bayésien/MDL les note contre les paires d'entraînement.

Le vérifieur est le cœur du projet : une hypothèse n'est acceptée que si
elle reproduit exactement toutes les paires d'entraînement et qu'elle est la
plus courte (au sens MDL) parmi les survivantes. La solution livrée est donc
un **programme lisible**, pas une grille sortie d'une boîte noire — c'est ce
qui rend le solveur explicable, auditable, et améliorable échec par échec.

L'EPIC-0 (ce code) pose la fondation : mesurer avant de progresser. Un
harness d'évaluation scellé (splits dev/validation/final, le final étant
verrouillé programmatiquement) et deux baselines honnêtes — LLM direct
(Haiku, Sonnet, prompts gelés) et brute-force sur une DSL de 10 primitives —
donnent les chiffres à battre et la courbe de scaling de l'oracle.

Spec détaillée : tickets Linear X-50 → X-57, projet
[SOLVEUR — ARC-AGI explicable](https://linear.app/productailab/project/solveur-arc-agi-explicable).

## Démarrage sur machine vierge

Prérequis : Python ≥ 3.11 et [uv](https://docs.astral.sh/uv/).

```bash
cd solveur
make install        # uv sync — crée .venv et installe les deps du lockfile
make test           # pytest
make eval ARGS="--help"
```

## Lancer une évaluation

```bash
make eval ARGS="--solver brute --split dev"      # baseline brute-force
make report ARGS="--run <run_id>"                # rapport Markdown dans reports/
```

Les runs sont journalisés dans `runs.db` (SQLite, non committé). Le split
`final` est verrouillé : y accéder sans `FINAL_RUN=1` lève
`FinalSetLockedError` — voir `CLAUDE.md`, règle 3.
