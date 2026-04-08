.PHONY: lint format test run

lint:
	isort . --check-only --diff
	black . --check
	flake8 .

format:
	isort .
	black .

test:
	pytest

run:
	uvicorn app.main:app --reload
