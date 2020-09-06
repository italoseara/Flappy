PYTHON := python3

run:
	$(PYTHON) src/main.py

check:
	@pylint -j 4 $$(find src -type f | grep '\.py$$')

pip:
	$(PYTHON) -m pip install pygame
	$(PYTHON) -m pip install pylint
