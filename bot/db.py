from contextlib import asynccontextmanager
from typing import AsyncContextManager

from conf.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    settings.ASYNC_DATABASE_URL, pool_size=50, max_overflow=99, pool_pre_ping=True
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def async_db_connection() -> AsyncContextManager[AsyncSession]:
    async with async_session() as session:
        yield session
