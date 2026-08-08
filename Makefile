.PHONY: check build serve

check:
	python scripts/check_wiki.py

build: check
	mkdocs build --strict

serve: check
	mkdocs serve
