ENV = PYTHONPATH=.

run\:%:
	${ENV} python3 greenworld/scripts/$(subst run:,,$@).py