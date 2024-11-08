up:
	docker compose up --build

deploy:
	git pull
	docker compose up --build --force-recreate -d

run: up

local:
	docker compose -f local-docker-compose.yml up -d
	cd app; poetry run alembic upgrade head; \
	poetry run uvicorn app.main:app --port 8000 --reload

migrations:
	cd app; poetry run alembic revision --autogenerate -m $(m)

migrate:
	cd app; poetry run alembic upgrade head

test:
	docker compose -f test-docker-compose.yml up -d
	docker build -t test_template:latest --file ./app/test.Dockerfile ./app
	- docker run --network test-template --env-file ./app/production.example.env test_template:latest alembic upgrade head && pytest
	docker compose -f test-docker-compose.yml down

lint:
	cd app; poetry run ruff check app; poetry run mypy app

format:
	cd app; poetry run ruff format app

.DEFAULT_GOAL := local
