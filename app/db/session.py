# app/db/session.py
from typing import AsyncIterator

from sqlalchemy import create_engine

from app.core.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
)

sync_engine = create_engine(
    settings.SYNC_DATABASE_URL,
    echo=settings.DB_ECHO,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        yield session
