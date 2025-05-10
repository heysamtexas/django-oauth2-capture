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

.PHONY: prerelease
prerelease: ## Run checks before releasing
	ruff --config pyproject.toml check .
	# Add any other pre-release checks here
	@echo "Pre-release checks passed! Ready to run 'make release'"

.PHONY: release
release: ## Create a new release with commitizen and push to GitHub
	cz bump --yes
	git push
	git push --tags

.PHONY: release-dry-run
release-dry-run: ## Show what version would be bumped to
	cz bump --dry-run
