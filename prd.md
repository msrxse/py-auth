# py-auth — FastAPI Authentication & Authorization Showcase

## Goal

Build a FastAPI project from scratch that demonstrates **authentication** (who are you?) and **authorization** (what can you do?) using modern best practices.

## Decisions Made

| Decision | Choice | Why |
|---|---|---|
| Auth approach | From scratch | Educational — understand every layer |
| Database | PostgreSQL | Production-grade |
| ORM | SQLAlchemy async | Modern FastAPI pattern |
| Migrations | Alembic | Industry standard |
| Auth model | RBAC + granular permissions | Roles hold permissions; code checks permissions, not roles |
| JWT library | PyJWT | Maintained (python-jose is abandoned) |
| Password hashing | pwdlib[argon2] | Maintained (passlib is deprecated), Argon2id is best |
| Token strategy | Access token (short) + Refresh token (long) | Security best practice |
| Permission storage | Database (not in JWT) | Permissions can change without reissuing tokens |
| Frontend permissions | Returned in `/users/me` response | Frontend uses for UI rendering; backend always re-validates |

## Authorization Architecture

```
JWT contains:  { sub: user_id, exp: ... }     ← identity only
Database holds: Users → Roles → Permissions    ← source of truth

Flow:
  Request → decode JWT → get user_id → query DB for permissions → allow/deny
```

**Why not put permissions in the JWT?**
- Permissions can be revoked instantly (no waiting for token expiry)
- No token bloat (users with many permissions)
- Database is always the source of truth

## Database Schema

```
Users ──many-to-many──► Roles ──many-to-many──► Permissions
  │
  └── RefreshTokens (one-to-many)
```

## Demo Resources

- **Articles**: CRUD gated by permissions (`create_article`, `read_article`, `update_article`, `delete_article`)
- **User management**: Admin-only operations (`read_user`, `update_user`, `delete_user`)

## Default Roles

| Role | Permissions |
|---|---|
| viewer | `read_article`, `read_user` |
| editor | viewer + `create_article`, `update_article` |
| admin | all permissions |

---

## Task List

We will build this project step by step:

### Phase 1: Foundation
- [x] **Task 1 — Project setup**: FastAPI hello-world in `backend/`, requirements.txt, venv
- [x] **Task 2 — Database & config**: PostgreSQL via Docker, pydantic-settings, async SQLAlchemy engine, .env
- [x] **Task 3 — Models**: User, Role, Permission, RefreshToken, Article + join tables
- [ ] **Task 4 — Alembic migrations**: Initialize Alembic, generate first migration, seed default roles/permissions

### Phase 2: Authentication
- [ ] **Task 5 — Registration**: `POST /auth/register` — create user, hash password, assign default role
- [ ] **Task 6 — Login**: `POST /auth/login` — verify credentials, return access + refresh tokens
- [ ] **Task 7 — Token refresh**: `POST /auth/refresh` — issue new access token using refresh token
- [ ] **Task 8 — Current user**: `GET /users/me` — return user profile with roles and permissions

### Phase 3: Authorization
- [ ] **Task 9 — Auth dependencies**: Build `get_current_user`, `require_permission()`, `require_role()` dependencies
- [ ] **Task 10 — Articles CRUD**: Protected endpoints with per-action permission checks
- [ ] **Task 11 — User management**: Admin-only endpoints to list/update/delete users

### Phase 4: Hardening
- [ ] **Task 12 — Logout & token revocation**: Revoke refresh tokens on logout
- [ ] **Task 13 — Error handling**: Consistent error responses for 401/403
- [ ] **Task 14 — Tests**: Pytest tests for auth flows and permission checks

---

## Tech Stack

- **Python 3.11+**
- **FastAPI** — web framework
- **SQLAlchemy 2.x** — async ORM
- **Alembic** — migrations
- **PyJWT** — JWT tokens
- **pwdlib[argon2]** — password hashing
- **pydantic-settings** — configuration from .env
- **asyncpg** — async PostgreSQL driver
- **pytest + httpx** — testing

---

## Project Structure

```
py-auth/
  README.md
  prd.md
  docker-compose.yml           ← PostgreSQL container
  .vscode/settings.json
  backend/
    requirements.txt
    .env                       ← local secrets (gitignored)
    .env.example               ← template for other devs
    venv/
    app/
      __init__.py
      main.py              ← FastAPI entry point
      core/
        config.py          ← pydantic-settings (.env)
        database.py        ← async SQLAlchemy engine/session
      auth/
        router.py          ← /auth/register, /auth/login, /auth/refresh
        schemas.py         ← Pydantic models (request/response)
        models.py          ← User, Role, Permission, RefreshToken
        dependencies.py    ← get_current_user, require_permission()
        service.py         ← business logic (authenticate, create tokens)
      articles/
        router.py
        schemas.py
        models.py
        service.py
      users/
        router.py
        schemas.py
        service.py
```
