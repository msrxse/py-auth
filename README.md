# py-auth

FastAPI authentication & authorization showcase.

## Database

Start PostgreSQL via Docker:

```bash
docker compose up -d
```

Stop it:

```bash
docker compose down
```

Connection: `postgresql://pyauth:pyauth@localhost:5432/pyauth`

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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

## Run

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

API available at http://localhost:8000

Health check: http://localhost:8000/health
