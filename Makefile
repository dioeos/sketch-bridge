DEV_YML := docker-compose.dev.yml
UV_ENV := ../.env

include .env

.PHONY: help
help:
	@echo "make help 								Show this help message"
	@echo "make dev 								Run the app in development mode"
	@echo "make clean 							Remove and clean dev containers"
	@echo "make client-shell				Enter bash shell in temp dev client"
	@echo "make server-shell				Enter bash shell in temp dev server"
	@echo "make revision						Create new Alembic revision locally"
	@echo "make reset db						Recreate DB and upgrade alembic head"

dev:
	docker-compose -f $(DEV_YML) up

test:
	cd server && PYTHONPATH=./ uv run pytest

build:
	docker-compose -f $(DEV_YML) build

clean:
	docker-compose -f $(DEV_YML) down

client-shell:
	docker-compose -f $(DEV_YML) run --rm client \
		sh

server-shell:
	docker-compose -f $(DEV_YML) run --rm server \
		sh

revision:
	@if [ -z "$(msg)"]; then \
		echo "Missing MSG: make revision msg=\'message'"; \
		exit 1; \
	fi; \
	cd server && uv run --env-file $(UV_ENV) alembic revision --autogenerate -m "$(msg)"

upgrade:
	cd server && uv run --env-file $(UV_ENV) alembic upgrade head

reset-db:
	docker-compose -f $(DEV_YML) down -v
	docker-compose -f $(DEV_YML) up -d

	until docker-compose -f $(DEV_YML) exec -T postgres_db pg_isready -U ${DATABASE__USERNAME} -d ${DATABASE__DB} >/dev/null 2>&1; do \
		echo "Checking Postgres status..."; \
		sleep 1; \
	done

	docker-compose -f $(DEV_YML) exec server uv run alembic upgrade head
	docker-compose -f $(DEV_YML) logs -f




