SHELL := /bin/bash

init:
	python3 -m venv .venv
	poetry install --with dev
	poetry run pre-commit install
	poetry env info
	@echo "Created virtual environment"

test:
	poetry run pytest --cov=src/ --cov-report=term-missing --no-cov-on-fail --cov-report=xml --cov-fail-under=90
	rm .coverage

lint:
	poetry run ruff format
	poetry run ruff check --fix

typecheck:
	poetry run mypy src/ tests/ --ignore-missing-imports

format:
	make lint
	make typecheck

update:
	poetry cache clear pypi --all
	poetry update

docker:
	docker build --no-cache -f Dockerfile -t exo_oscilloscope-smoke .
	docker run --rm exo_oscilloscope-smoke

app:
	poetry run python -m exo_oscilloscope --stderr-level DEBUG --log-level DEBUG
