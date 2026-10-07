.PHONY: api test lint setup

setup:
	cd ../.. && uv sync

api:
	cd ../.. && uv run uvicorn apps.api.radar_api.main:app --reload

test:
	cd ../.. && uv run pytest apps/api/tests

lint:
	cd ../.. && uv run ruff check apps/api
	cd ../.. && uv run mypy apps/api
