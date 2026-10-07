.PHONY: radar test lint setup api web

setup:
	uv sync
	npm install

radar:
	@if [ -z "$(WEEK)" ]; then echo "Uso: make radar WEEK=YYYY-MM-DD"; exit 1; fi
	uv run python scripts/new_radar_week.py --week $(WEEK)

test:
	uv run pytest apps/api/tests

lint:
	uv run ruff check apps/api scripts
	uv run ruff format --check apps/api scripts
	uv run mypy apps/api scripts

api:
	uv run uvicorn apps.api.radar_api.main:app --reload

web:
	npm run web:dev

release: test lint
	uv run python scripts/validate_signals.py
	uv run python scripts/build_data.py
	npm run web:build

