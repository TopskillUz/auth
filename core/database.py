from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings
from models.basic import Base

DATABASE_URL = "postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{DATABASE_PORT}/{POSTGRES_DB}".format(
    POSTGRES_USER=settings.POSTGRES_USER,
    POSTGRES_PASSWORD=settings.POSTGRES_PASSWORD,
    POSTGRES_HOST=settings.POSTGRES_HOST,
    DATABASE_PORT=settings.DATABASE_PORT,
    POSTGRES_DB=settings.POSTGRES_DB
)

engine = create_async_engine(DATABASE_URL)

Base = declarative_base(cls=Base)


def async_session_generator():
    return sessionmaker(
        engine, class_=AsyncSession
    )


#
# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session():
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
