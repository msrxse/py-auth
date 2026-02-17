# Alembic Migrations

Generic single-database configuration with an async dbapi.

All commands run from the `backend/` directory.

## Common Commands

### Apply all migrations

```
alembic upgrade head
```

### Rollback one migration

```
alembic downgrade -1
```

### Rollback all migrations

```
alembic downgrade base
```

### Show current revision

```
alembic current
```

### Show migration history

```
alembic history --verbose
```

### Auto-generate a new migration after model changes

```
alembic revision --autogenerate -m "description of changes"
```

### Seed roles and permissions

```
python -m app.seed
```

## Verify a Migration Was Applied

Check that the DB is at the latest revision:

```
alembic current
```

If current matches head, you're up to date.

You can also run autogenerate to confirm nothing is out of sync:

```
alembic revision --autogenerate -m "should be empty"
```

If `upgrade()` is empty, your DB matches your models. Delete the file afterward.

Check the actual tables in Postgres:

```
# docker exec -it <postgres_container> psql -U <user> -d <db> -c "\dt"

docker exec -it py-auth-db psql -U pyauth -d pyauth -c "\dt"
```

## Typical Workflow

1. Edit a model (e.g. add a column to User)
2. Auto-generate the migration:
   ```
   alembic revision --autogenerate -m "add bio to users"
   ```
3. Review the generated file in `alembic/versions/`
4. Apply it:
   ```
   alembic upgrade head
   ```
