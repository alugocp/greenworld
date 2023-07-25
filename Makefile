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

ui:
	$(NPM_BIN)/tsc -p server/tsconfig.json

serve: ui
	$(ENV) $(PYTHON) server/app.py

test:
	$(PYTHON) -m pytest

%:
	$(ENV) $(PYTHON) greenworld/scripts/$@.py $(subst $(COMMA),$(SPACE),$(FILES))