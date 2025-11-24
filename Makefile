DEV_YML := docker-compose.dev.yml

.PHONY: help
help:
	@echo "make help 								Show this help message"
	@echo "make dev 								Run the app in development mode"
	@echo "make dev-clean 					Remove and clean dev containers"
	@echo "make dev-client-shell		Enter bash shell in temp dev client"
	@echo "make dev-server-shell		Enter bash shell in temp dev server"

dev:
	docker-compose -f $(DEV_YML) up

dev-clean:
	docker-compose -f $(DEV_YML) down


dev-client-shell:
	docker-compose -f $(DEV_YML) run --rm client \
		sh

dev-server-shell:
	docker-compose -f $(DEV_YML) run --rm server \
		sh
