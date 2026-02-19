from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.auth.router import router as auth_router
from app.core.database import engine
from app.users.router import router as users_router


# lifespan = a FasAPI livecycle hook. Code before yield runs in startup - after in shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verify database connection on startup
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    yield
    await engine.dispose()


app = FastAPI(title="py-auth", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(users_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
