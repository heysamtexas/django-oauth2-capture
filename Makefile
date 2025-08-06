.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: bootstrap
bootstrap: ## Setup development environment with uv
	uv sync --dev

.PHONY: prerelease
prerelease: ## Run checks before releasing
	uv run ruff check .
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
