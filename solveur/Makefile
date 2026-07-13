# SOLVEUR — cibles standard. Tout se lance depuis le dossier solveur/.
.PHONY: install lint test eval report

install:
	uv sync

lint:
	uv run ruff check .
	uv run mypy solveur

test:
	uv run pytest tests/ -q

# Usage : make eval ARGS="--solver brute --split dev"
eval:
	uv run python -m solveur.eval $(ARGS)

# Usage : make report ARGS="--run <run_id>"
report:
	uv run python -m solveur.report $(ARGS)
