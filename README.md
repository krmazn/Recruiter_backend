# FastAPI + Async SQLAlchemy template

## Local environment
### Installation
#### FastAPI app
1. Install Python 3.12

2. Install poetry >=1.8:

https://python-poetry.org/docs/#installation 


3. Choose python3.12 for Poetry

https://python-poetry.org/docs/managing-environments/#switching-between-environments

```bash
cd app
poetry env use 3.12
```

4. Install requirements

```bash
poetry install --with dev
```

Pin packages versions after initializing the project.

5. Copy .env
```bash
cp local.example.env .env
```

#### Docker
Refer to:

https://docs.docker.com/engine/install/

### Usage

1. Start PSQL in Docker Compose:
```bash
docker compose -f local-docker-compose.yml up -d
```

2. Apply migrations:
```bash
cd app
poetry run alembic upgrade head
```

3. Run Uvicorn server:
```bash
poetry run uvicorn app.main:app --port 8000 --reload
```

OR use a shortcut script:

```bash
make local
```

### Migrations
Powered by Alembic

Create a migration:
```bash
cd app
poetry run alembic revision --autogenerate -m add_field
```

Migrate:
```bash
poetry run alembic upgrade head
```

### Linting and formatting
Use `ruff` and `mypy` with config from `app/pyproject.toml`:

Lint:
```bash
poetry run ruff check app
poetry run mypy check app
```

Format:
```bash
poetry run ruff format app
```

## API Docs
Swagger UI is available at `GET /api/docs` when the server is running.

## Testing

Run tests in Docker with Pytest:

```bash
make test
```

## Production environment

### Installation
Copy and configure .env:

```bash
cp app/production.example.env app/.env
```

### Usage

```bash
make up
```
# Recruiter_backend
