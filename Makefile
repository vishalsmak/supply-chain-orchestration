SHELL := /bin/bash

env-setup:
	rm -rf venv
	# Python 3.9.12
	python3.9 -m venv venv; \
	source venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r src/setup/requirements.txt

run-local:
	source venv/bin/activate; \
	python src/run.py
