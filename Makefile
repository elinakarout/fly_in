.PHONY: install run debug clean lint lint-strict

PYTHON := python3
PIP := pip3
MAIN := src
CONFIG := config.txt

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	flake8 $(FILES)
	mypy $(FILES)

lint-strict:
	flake8 $(FILES)
	mypy $(FILES) --strict
