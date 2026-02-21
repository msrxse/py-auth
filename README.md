# py-auth

FastAPI authentication & authorization showcase.

See [backend/README.md](backend/README.md) for setup, migrations, running, and API examples.

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

## CI Pipeline

Test the GitHub Actions workflow locally with [act](https://github.com/nektos/act):

```bash
make ci
```
