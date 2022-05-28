from typing import List

from models.user import User
from sqlalchemy import select
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression


async def get_user(
    conn: AsyncSession, filters: List[BinaryExpression]
) -> ChunkedIteratorResult:
    return await conn.execute(select(User).where(*filters))
