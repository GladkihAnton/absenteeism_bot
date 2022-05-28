import asyncio
from typing import List, Optional

from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from crud.filters.user import get_user_filters
from crud.user import create_user, get_user
from db import async_db_connection
from models import User
from roles import ADMIN
from state.admin import AdminState
from state.employee import EmployeeState
from template.loader import render_template


async def cmd_start(message: Message, state: FSMContext):
    filters = get_user_filters(user_id=message.chat.id)
    async with async_db_connection() as conn:
        user: Optional[User] = (await get_user(conn, filters)).scalar()
        if not user:
            await create_user(
                conn,
                telegram_user_id=message.from_user.id,
                name=message.from_user.full_name,
            )
            await conn.commit()

            await _send_user_request_to_admins(conn, message)
            await message.answer(render_template("error/user_non_active.jinja2"))

        if not user.active:
            await message.answer(render_template("error/user_non_active.jinja2"))


async def cmd_menu(message: Message, ctx: FSMContext):
    pass


async def _send_user_request_to_admins(conn: AsyncSession, message: Message) -> None:
    filters = get_user_filters(role=ADMIN)
    users: List[User] = (await get_user(conn, filters, with_role=True)).scalars().all()

    text = render_template(
        "new_user_request.jinja2", username=message.from_user.username
    )
    send_message_tasks = [
        message.bot.send_message(chat_id=user.telegram_user_id, text=text)
        for user in users
    ]

    await asyncio.gather(*send_message_tasks)


async def _get_handlers(message: Message, ctx: FSMContext):
    async with async_db_connection() as conn:
        cond = get_user_filters(telegram_user_id=message.from_user.id)
        user = await get_user(conn, cond, True)
        match user.role.name:
            case "admin":
                text = "Добро пожаловать, вы вошли как администратор, воспользуйтесь меню"
                state = AdminState.START
                markup = ReplyKeyboardRemove()
            case "employee":
                text = "Добро пожаловать, воспользуйтесь меню"
                state = EmployeeState.START
                markup = ReplyKeyboardRemove()
            case _:
                raise Exception()

        await ctx.set_state(state)
        await message.answer(text, reply_markup=markup)


def register_handlers_auth(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_menu, commands="start", state="*")
