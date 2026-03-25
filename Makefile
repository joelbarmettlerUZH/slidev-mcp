.PHONY: install bootstrap lint lint-fix format format-check test test-all pr-ready \
        serve docker-build docker-dev-up docker-dev-down docker-prod-up docker-prod-down \
        docs-install docs-dev docs-build docs-preview

install:
	uv sync

bootstrap:
	scripts/bootstrap.sh
	python3 scripts/fetch-theme-readmes.py

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

test:
	uv run pytest

test-all:
	uv run pytest -m ""

test-integration:
	docker compose -f docker-compose.dev.yml up -d
	uv run pytest -m integration
	docker compose -f docker-compose.dev.yml down

pr-ready: lint-fix format test

serve:
	uv run python -m slidev_mcp.server

docker-build:
	docker build -t slidev-mcp-server -f docker/Dockerfile.mcp .
	docker build -t slidev-mcp-builder -f builder/Dockerfile builder/

docker-dev-up:
	docker compose -f docker-compose.dev.yml up -d

docker-dev-down:
	docker compose -f docker-compose.dev.yml down

docker-local-up:
	docker compose -f docker-compose.local.yml up -d

docker-local-down:
	docker compose -f docker-compose.local.yml down

docker-prod-up:
	docker compose -f docker-compose.prod.yml up -d

docker-prod-down:
	docker compose -f docker-compose.prod.yml down

docs-install:
	cd docs && bun install

docs-dev:
	cd docs && bun run dev

docs-build:
	cd docs && bun run build

docs-preview:
	cd docs && bun run preview
