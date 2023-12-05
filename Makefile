.PHONY: install
install:
	poetry config virtualenvs.create true && poetry config virtualenvs.in-project true && poetry install --no-interaction --no-ansi

.PHONY: run
run:
	poetry run streamlit run examples/1_🏠_Home.py
