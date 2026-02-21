# Backend

## Activate Virtual Environment

From the `backend` folder, run:

```bash
source .venv/bin/activate
```

To deactivate:

```bash
deactivate
```

## Setup

```bash
poetry install
```

## Migrations

```bash
# Apply all migrations
alembic upgrade head

# Generate a new migration after changing models
alembic revision --autogenerate -m "description"

# Seed default roles and permissions
python -m app.seed
```

See [alembic/README.md](alembic/README.md) for the full list of migration commands, verification steps, and seeding details.

## Run

```bash
uvicorn app.main:app --reload
```

API available at http://localhost:8000

Health check: http://localhost:8000/health

## Linting

```bash
ruff check .        # lint
ruff format .       # format
```

Pre-commit hooks run both automatically on every commit. To set up:

```bash
pre-commit install
```

## API Examples

Register a new user:

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
```

Login:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```
