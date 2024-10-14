# Variables
NAME ?=my_project
DJANGO_APP ?=oauth_connector
ENV_DIR ?=.venv


.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.venv/:
	python -m venv .venv/

.PHONY: bootstrap
bootstrap: .venv/
	$(ENV_DIR)/bin/pip install --upgrade pip
	$(ENV_DIR)/bin/pip install -r requirements.txt
	$(ENV_DIR)/bin/pip install -r requirements-dev.txt
	$(ENV_DIR)/bin/pip install -e .

# Create a new Django project and reusable app
new_project: install
	mkdir -p $(NAME)
	$(ENV_DIR)/bin/python3 manage.py startapp $(NAME)
	$(ENV_DIR)/bin/pip install -e ../$(NAME)

	$(ENV_DIR)/bin/python3 manage.py migrate


.PHONY: new_project clean
