.PHONY: install run debug clean lint lint-strict

PYTHON := python3
PIP := pip3
MAIN := main.py
CONFIG := config.txt
ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

EASY1 = maps/easy/01_linear_path.txt
EASY2 = maps/easy/02_simple_fork.txt
EASY3 = maps/easy/03_basic_capacity.txt
MEDIUM1 = maps/medium/01_dead_end_trap.txt
MEDIUM2 = maps/medium/02_circular_loop.txt
MEDIUM3 = maps/medium/03_priority_puzzle.txt
HARD1 = maps/hard/01_maze_nightmare.txt
HARD2 = maps/hard/02_capacity_hell.txt
HARD3 = maps/hard/03_ultimate_challenge.txt
CHALLENGER = maps/challenger/01_the_impossible_dream.txt

MAP ?= EASY1

ifeq ($(MAP),EASY1)
ARGS = $(EASY1)

else ifeq ($(MAP),EASY2)
ARGS = $(EASY2)

else ifeq ($(MAP),EASY3)
ARGS = $(EASY3)

else ifeq ($(MAP),MEDIUM1)
ARGS = $(MEDIUM1)

else ifeq ($(MAP),MEDIUM2)
ARGS = $(MEDIUM2)

else ifeq ($(MAP),MEDIUM3)
ARGS = $(MEDIUM3)

else ifeq ($(MAP),HARD1)
ARGS = $(HARD1)

else ifeq ($(MAP),HARD2)
ARGS = $(HARD2)

else ifeq ($(MAP),HARD3)
ARGS = $(HARD3)

else ifeq ($(MAP),CHALLENGER)
ARGS = $(CHALLENGER)

endif

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
	flake8 . --exclude=fly_in
	mypy .

lint-strict:
	flake8 . --exclude=fly_in
	mypy . --strict

.PHONY: install run $(ARGS) debug clean lint lint-strict
