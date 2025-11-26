DEV_YML := docker-compose.dev.yml
UV_ENV := ../.env

include .env

.PHONY: help

help:
	@echo "make help 								Show this help message"
	@echo "make dev 								Run the app in development mode"
	@echo "make test 								Run pytest for server"
	@echo "make build								Build docker containers"
	@echo "make psql msg=(msg)			Execute PSQL command in Docker Postgres DB"
	@echo "make clean 							Remove and clean dev containers"
	@echo "make client-shell				Enter bash shell in temp dev client"
	@echo "make server-shell				Enter bash shell in temp dev server"
	@echo "make revision						Create new Alembic revision"
	@echo "make upgrade							Upgrade alembic head"
	@echo "make reset db						Recreate DB and upgrade alembic head"

dev:
	docker-compose -f $(DEV_YML) up

test:
	cd server && PYTHONPATH=./ uv run pytest

build:
	docker-compose -f $(DEV_YML) build

psql:
	@if [ -z "$(msg)"]; then \
		echo "Missing MSG: make psql msg=\'message'"; \
		exit 1; \
	fi; \
	docker-compose -f $(DEV_YML) exec postgres_db psql -U sketchbridge-admin -d sketchbridge_db -c "$(msg)"

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
	docker-compose -f $(DEV_YML) exec server uv run alembic revision --autogenerate -m "$(msg)"

upgrade:
	docker-compose -f $(DEV_YML) exec server uv run alembic upgrade head

reset-db:
	docker-compose -f $(DEV_YML) down -v
	docker-compose -f $(DEV_YML) up -d

	until docker-compose -f $(DEV_YML) exec -T postgres_db pg_isready -U ${DATABASE__USERNAME} -d ${DATABASE__DB} >/dev/null 2>&1; do \
		echo "Checking Postgres status..."; \
		sleep 1; \
	done

	docker-compose -f $(DEV_YML) exec server uv run alembic upgrade head
	docker-compose -f $(DEV_YML) logs -f




