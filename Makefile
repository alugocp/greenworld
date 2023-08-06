SCRIPTS := $(patsubst greenworld/scripts/%.py, %, $(shell ls greenworld/scripts/*.py))
ENV := PYTHONPATH=.
PYTHON := python3
NPM_BIN := ./node_modules/.bin
COMMA:= ,
EMPTY:=
SPACE:= $(EMPTY) $(EMPTY)

lint: lint-ts lint-py lint-jinja

lint-py:
	$(ENV) $(PYTHON) -m pylint $(shell git ls-files "*.py")

lint-ts:
	$(NPM_BIN)/eslint frontend

lint-jinja:
	$(ENV) $(PYTHON) -m djlint server/templates --profile=jinja

install:
	$(PYTHON) -m pip install -r requirements.txt
	# Rscript scripts/packages.r

ui:
	$(NPM_BIN)/tsc -p server/tsconfig.json

serve: ui
	$(ENV) $(PYTHON) server/app.py

test: test-ts test-py

test-ts:
	npx ts-mocha -p frontend/tests/tsconfig.json frontend/tests/*.ts

test-py:
	$(PYTHON) -m pytest

$(SCRIPTS):
	$(ENV) $(PYTHON) greenworld/scripts/$@.py $(subst $(COMMA),$(SPACE),$(FILES))