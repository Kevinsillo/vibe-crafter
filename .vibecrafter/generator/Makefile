.PHONY: install deps test lint format run seed clean

install:
	pip install poetry
	poetry config virtualenvs.in-project true

deps:
	poetry install

test:
	poetry run pytest

lint:
	poetry run ruff check src/ tests/

format:
	poetry run ruff format src/ tests/

run:
	poetry run python main.py

seed:
	rm -f steps.db
	sqlite3 steps.db < seed.sql

clean:
	rm -f steps.db
