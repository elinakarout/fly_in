.PHONY: install run debug clean lint lint-strict

PYTHON := python3
PIP := pip3
MAIN := main.py
CONFIG := config.txt
ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(ARGS)

$(eval $(ARGS):;@:)

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	flake8 .
	mypy .

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run $(ARGS) debug clean lint lint-strict
