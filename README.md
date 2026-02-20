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

### Schema

```mermaid
erDiagram
    users ||--o{ user_roles : has
    users ||--o{ refresh_tokens : has
    users ||--o{ articles : authors
    roles ||--o{ user_roles : has
    roles ||--o{ role_permissions : has
    permissions ||--o{ role_permissions : has

    users {
        int id PK
        string username UK
        string email UK
        string hashed_password
        bool is_active
        bool is_superuser
        datetime created_at
    }

    roles {
        int id PK
        string name UK
        string description
    }

    permissions {
        int id PK
        string name UK
        string resource
        string action
    }

    user_roles {
        int user_id FK
        int role_id FK
    }

    role_permissions {
        int role_id FK
        int permission_id FK
    }

    refresh_tokens {
        int id PK
        string token UK
        int user_id FK
        datetime expires_at
        bool revoked
        datetime created_at
    }

    articles {
        int id PK
        string title
        text content
        int author_id FK
        datetime created_at
        datetime updated_at
    }
```

## Setup

```bash
poetry install
```

## Migrations

```bash
# Apply all migrations
cd backend
alembic upgrade head

# Generate a new migration after changing models
alembic revision --autogenerate -m "description"

# Seed default roles and permissions
python -m app.seed
```

See [backend/alembic/README.md](backend/alembic/README.md) for the full list of migration commands, verification steps, and seeding details.

## Run

```bash
cd backend
uvicorn app.main:app --reload
```

## Linting

```bash
ruff check backend/        # lint
ruff format backend/       # format
```

Pre-commit hooks run both automatically on every commit. To set up:

```bash
pre-commit install
```

API available at http://localhost:8000

Health check: http://localhost:8000/health

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
