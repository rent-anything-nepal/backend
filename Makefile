include .env
SHELL=/bin/bash
ADMIN_EMAIL := admin@test.com
ADMIN_USERNAME := admin
ADMIN_PASSWORD := admin
PYTHON := $(PYTHON)
PIP := $(PYTHON) -m pip

.PHONY: fresh install freeze mg mm migrations dev shell cs superuser admin clean-db clean-mg clean black help

fresh: clean-db migrations admin ## Clean everything, install dependencies, run migrations and create admin user

install: ## Install dependencies
	$(PIP) install -r requirements.txt

freeze: ## Freeze dependencies
	$(PIP) freeze > requirements.txt

mg: ## Run migrations
	$(PYTHON) manage.py migrate --settings=$(SETTINGS)

mm: ## Make migrations for a specific app
	$(PYTHON) manage.py makemigrations $(app) --settings=$(SETTINGS)

migrations: ## Run thorough migrations of all available apps sequentially
	make mm app=account
	make mg
	make mm app=media
	make mm app=accommodation
	make mm app=review
	make mg

dev: ## Run development server
	$(PYTHON) manage.py runserver --settings=backend.settings.dev

shell: ## Run shell
	$(PYTHON) manage.py shell --settings=$(SETTINGS)

cs: ## Collect static files
	$(PYTHON) manage.py collectstatic --settings=$(SETTINGS)

superuser: ## Create superuser
	$(PYTHON) manage.py createsuperuser --settings=$(SETTINGS)

admin: ## Create configured admin user
	DJANGO_SUPERUSER_PASSWORD=$(ADMIN_PASSWORD) \
		$(PYTHON) manage.py createsuperuser \
		--username $(ADMIN_USERNAME) \
		--email $(ADMIN_EMAIL) \
		--noinput --settings=$(SETTINGS)

clean-db: ## Clean database, media and static files
	cp assets/org org -r
	rm -rf assets
	mkdir assets
	mv org assets/org
	rm -rf static
	rm -rf db.sqlite3

clean-mg: ## Clean migrations
	rm -rf **/migrations

clean: clean-db clean-mg ## Clean db related files and migration files

black: ## Run black
	black .

help: ## Display this help screen
	@echo
	@printf "\033[1mRent Anything Backend\033[0m\n"
	@echo ------------------------------------------
	@echo
	@echo Available commands:
	@echo
	@awk 'BEGIN {FS = ":.*##"; printf "\033[36m\033[0m"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
