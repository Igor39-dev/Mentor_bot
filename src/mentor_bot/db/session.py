"""Async SQLAlchemy engine and session factory."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from mentor_bot.config import get_settings

_settings = get_settings()

engine: AsyncEngine = create_async_engine(
    _settings.DATABASE_URL,
    pool_pre_ping=True,
)

async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide async database session as a context manager."""
    async with async_session_maker() as session:
        yield session
