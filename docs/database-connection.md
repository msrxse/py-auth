# Database Connection

How SQLAlchemy connects to the PostgreSQL container.

## 1. Docker exposes PostgreSQL on localhost

`docker-compose.yml` starts a Postgres container with user `pyauth`, password `pyauth`, database `pyauth`, and maps port `5432` inside the container to `5432` on your host machine. So from your host, Postgres is reachable at `localhost:5432`.

## 2. The connection string lives in `.env`

`backend/.env` has:

```
DATABASE_URL=postgresql+asyncpg://pyauth:pyauth@localhost:5432/pyauth
```

This is a standard SQLAlchemy URL format:

```
dialect+driver://user:password@host:port/database
```

- `postgresql` — dialect (tells SQLAlchemy it's Postgres)
- `asyncpg` — the async driver library that actually speaks the Postgres wire protocol
- `pyauth:pyauth` — username:password (matching what Docker sets)
- `localhost:5432` — where Docker is exposing the container
- `/pyauth` — the database name

## 3. Pydantic loads `.env` into a settings object

`backend/app/core/config.py` — `Settings` extends `BaseSettings` with `SettingsConfigDict(env_file=".env")`. When `settings = Settings()` runs, pydantic-settings reads `.env` and populates `settings.DATABASE_URL` with the connection string.

## 4. SQLAlchemy creates the engine (connection pool)

`backend/app/core/database.py` — `create_async_engine(settings.DATABASE_URL)` takes that URL and creates an **engine**. The engine is not a single connection — it's a **connection pool** that manages multiple connections so you don't open/close one per request.

## 5. Sessions wrap individual "conversations" with the DB

`async_sessionmaker(engine)` creates a factory for sessions. A session tracks your queries, modifications, and commits as a unit of work.

`get_db()` is a FastAPI dependency that opens a session, yields it to your route handler, then closes it automatically when the request is done.

## 6. FastAPI verifies the connection on startup

`backend/app/main.py` — The lifespan hook runs `SELECT 1` on startup to confirm the DB is actually reachable. On shutdown it calls `engine.dispose()` to close all pooled connections cleanly.

## The full flow

```
.env  →  Settings  →  create_async_engine(URL)  →  engine (pool)
                                                        ↓
docker-compose (Postgres on :5432)  ←──── asyncpg driver connects
                                                        ↓
                                              async_sessionmaker
                                                        ↓
                                          get_db() yields session to routes
```

SQLAlchemy itself never "discovers" the database — you give it the explicit URL, and `asyncpg` handles the actual TCP connection to the Postgres container on localhost.
