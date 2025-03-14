SRCPATH := $(CURDIR)
PROJECTNAME := $(shell basename $(CURDIR))

default: build run

.PHONY: help
help: 
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

# Installation
.PHONY: install-build
install-build:
	@# Help: Install dependencies required for building
	poetry install

.PHONY: lint
lint: lint-docker lint-python ## (Run all lint commands)

.PHONY: lint-python
lint-python: ## Lint Python files using Flake8
	flake8 . --ignore=F401

.PHONY: lint-docker 
lint-docker: ## Lint Docker files using hadolint
	hadolint Dockerfile

.PHONY: build 
build: ## Build Docker image and run vulnerability scan
	docker build -t dc-data-radar .
# grype dc-data-gen

.PHONY: run 
run: ## Run Docker image locally
	docker run -p 8050:8050 --rm dc-data-radar

local: local.sh
	$(shell . ./local.sh)
	
.PHONY: format 
format: ## Automatically format Python Files
	black .

.PHONY: clean 
clean: ## Remove temporary files
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
