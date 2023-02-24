ENV = PYTHONPATH=.
PYTHON = python3

run\:%:
	$(ENV) $(PYTHON) greenworld/scripts/$(subst run:,,$@).py

lint:
	$(ENV) $(PYTHON) -m pylint $(shell git ls-files "*.py")

install:
	$(PYTHON) -m pip install -r requirements.txt

serve:
	$(ENV) $(PYTHON) greenworld/server/app.py