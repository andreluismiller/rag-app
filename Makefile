.PHONY: up down build logs sync ingest eval fmt lint shell

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

sync:
	uv sync

ingest:
	docker compose exec app uv run python -m src.ingestion.ingest

eval:
	docker compose exec app uv run python -m src.evaluation.run_eval

fmt:
	uv run ruff format .

lint:
	uv run ruff check .

shell:
	docker compose exec app bash
