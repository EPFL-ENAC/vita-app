install:
	poetry install

test:
	poetry run pytest

lint:
	poetry run pre-commit run --all-files

doc:
	$(MAKE) -C docs clean html
