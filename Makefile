# .PHONY: activate
.ONESHELL:
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
# SHELL := /bin/bash

$(VENV): requirements.txt
	python3 -m venv $(VENV)
	touch $(VENV)

activate:
	@echo "To activate the virtual environment, run:"
	@echo "source $(VENV)/bin/activate"
	source $(VENV)/bin/activate


freeze:
	$(PIP) freeze > requirements.txt

pushReady:
	$(freeze)
	deactivate
	git add .