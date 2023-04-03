ENV := PYTHONPATH=.
PYTHON := python3
NPM_BIN := ./node_modules/.bin
COMMA:= ,
EMPTY:=
SPACE:= $(EMPTY) $(EMPTY)

lint: lint-py lint-ts

lint-py:
	$(ENV) $(PYTHON) -m pylint $(shell git ls-files "*.py")

lint-ts:
	$(NPM_BIN)/eslint greenworld/server/src

install:
	$(PYTHON) -m pip install -r requirements.txt

ui:
	$(NPM_BIN)/tsc -p tsconfig.json

serve: ui
	$(ENV) $(PYTHON) greenworld/server/app.py

%:
	$(ENV) $(PYTHON) greenworld/scripts/$@.py $(subst $(COMMA),$(SPACE),$(FILES))