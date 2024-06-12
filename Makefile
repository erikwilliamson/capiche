export PYTHONPATH = src
MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
BASE_DIR := $(dir $(MAKEFILE_PATH))
VENV_DIR := $(BASE_DIR).venv
SRC_DIR := $(BASE_DIR)src
ETC_DIR := $(BASE_DIR)etc
BIN_DIR := $(BIN_DIR)bin
PYTHON := /usr/local/bin/python3.12
PIP := /usr/local/bin/pip3.12

default: help

clear-screen:  # Clears the screen
	clear

test: clear-screen venv  # Runs all tests
	. $(VENV_DIR)/bin/activate; pytest --cov=capiche --cov-report term-missing --cov-report=html:doc/coverage -W ignore::DeprecationWarning

test-wip: clear-screen venv  # Runs selected tests
	. $(VENV_DIR)/bin/activate; pytest -m wip -W ignore::DeprecationWarning

clean-venv:  # Removes the existing venv
	rm -rf $(VENV_DIR)

venv: $(VENV_DIR)/touchfile  # Creates a new venv

$(VENV_DIR)/touchfile:
	test -d $(VENV_DIR) || $(PYTHON) -m venv --upgrade-deps $(VENV_DIR)
	. $(VENV_DIR)/bin/activate; pip install -U -r $(ETC_DIR)/requirements.txt -r $(ETC_DIR)/requirements.development.txt -r $(ETC_DIR)/requirements.testing.txt
	touch $(VENV_DIR)/touchfile

build:
	python -m build

upload-test:
	python3 -m twine upload --verbose --repository testpypi dist/*

upload:
	python3 -m twine upload dist/*

pyright:  # Runs pyright
	pyright

pylint:  # Runs pylint
	pylint src/capiche

ruff:  # Runs ruff
	ruff src

isort:  # Runs isort
	isort src

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
