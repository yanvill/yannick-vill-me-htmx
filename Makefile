include .env
export

lint:
	poetry run mypy server && poetry run ruff check --fix server

dev:
	poetry run server

install:
	poetry install
