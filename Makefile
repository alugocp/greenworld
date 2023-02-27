ENV := PYTHONPATH=.
PYTHON := python3
COMMA:= ,
EMPTY:=
SPACE:= $(EMPTY) $(EMPTY)

lint:
	$(ENV) $(PYTHON) -m pylint $(shell git ls-files "*.py")

install:
	$(PYTHON) -m pip install -r requirements.txt

serve:
	$(ENV) $(PYTHON) greenworld/server/app.py

%:
	$(ENV) $(PYTHON) greenworld/scripts/$@.py $(subst $(COMMA),$(SPACE),$(FILES))