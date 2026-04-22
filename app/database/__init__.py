import os
from typing import Callable
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database.models import Base
from dotenv import load_dotenv

load_dotenv()

engine = create_async_engine(
    "postgresql+asyncpg://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"
)

session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def database(func: Callable) -> Callable:
    '''Injects an async database session into the decorated function'''
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with session_maker() as session:
            kwargs["session"] = session
            return await func(*args, **kwargs)
    return wrapper