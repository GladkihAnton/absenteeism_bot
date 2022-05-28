from typing import List

from models.user import User
from sqlalchemy import insert, select
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.elements import BinaryExpression


async def get_user(
    conn: AsyncSession, filters: List[BinaryExpression], with_role: bool = False
) -> ChunkedIteratorResult:
    query = select(User).where(*filters)
    if with_role:
        query = query.options(joinedload(User.role, innerjoin=True))

    return await conn.execute(query)


async def create_user(conn: AsyncSession, **values) -> ChunkedIteratorResult:
    return await conn.execute(insert(User).values(**values))
