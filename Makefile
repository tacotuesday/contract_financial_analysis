#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = contract_financial_analysis
PYTHON_VERSION = 3.13
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

.PHONY: requirements clean lint format create_environment data test profile features pipeline

## Install Python Dependencies
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf data/interim/*
	rm -rf data/processed/*
	rm -rf models/*
	rm -rf reports/figures/*
	rm -rf logs/*


## Lint using flake8 and black (use `make format` to do formatting)
lint:
	flake8 ecommerce_pipeline tests
	isort --check --diff --profile black ecommerce_pipeline
	black --check --config pyproject.toml ecommerce_pipeline


## Format source code with black
format:
	black --config pyproject.toml ecommerce_pipeline


## Set up python interpreter environment
create_environment:
	
	conda create --name $(PROJECT_NAME) python=$(PYTHON_VERSION) -y
	
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"


# Generate data
data:
	python -c "from cfa.dataset import generate_contract_data; generate_contract_data()"


# Run data profiling
profile:
	python -m ecommerce_pipeline.profiling



# Run tests
test:
	pytest tests/


# Generate features
features:
	python -m ecommerce_pipeline.features


# Run end-to-end pipeline
pipeline:
	python -m ecommerce_pipeline.pipeline


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
