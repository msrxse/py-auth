from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# the database pool (manages pool connections so you are not opening/closing one per request)
engine = create_async_engine(settings.DATABASE_URL)

# creates database sessions: a session is like conversation with the DB - you query,modify,commit and it tracks changes.
async_session = async_sessionmaker(engine, expire_on_commit=False)


# All your SQLAlchemy models will inherit from this
class Base(DeclarativeBase):
    pass

# Some routes need this
async def get_db():
    async with async_session() as session:
        yield session
