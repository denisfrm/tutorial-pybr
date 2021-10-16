start:
	uvicorn --reload api_pedidos.api:app

format:
	poetry run isort . && poetry run black .

lint:
	poetry run flake8 .

test:
	python -m pytest
