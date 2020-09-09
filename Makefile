PYTHON := python3

run:
	$(PYTHON) src/main.py

check:
	@PYGAME_HIDE_SUPPORT_PROMPT=1 pylint -j 4 $$(find src -type f | grep '\.py$$')

pip:
	$(PYTHON) -m pip install pygame
