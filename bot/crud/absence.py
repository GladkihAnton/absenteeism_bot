from typing import List

from sqlalchemy.dialects import postgresql

from models.absence import Absence

from sqlalchemy import select
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression


async def get_absence(
    conn: AsyncSession, filters: List[BinaryExpression]
) -> ChunkedIteratorResult:
    return await conn.execute(select(Absence).where(*filters))


async def create_absence(conn: AsyncSession, **values) -> ChunkedIteratorResult:
    insert_stmt = postgresql.insert(Absence).values(**values)

    update_stmt = insert_stmt.on_conflict_do_update(
        index_elements=[Absence.telegram_user_id, Absence.date],
        set_={field: insert_stmt.excluded.get(field) for field in ['message']},
    )
    return await conn.execute(update_stmt)
