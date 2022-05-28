import asyncio
from typing import Any, Callable, Coroutine, Dict, List, Optional

from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from crud.filters.user import get_user_filters
from crud.user import create_user, get_user
from db import async_db_connection
from models import User
from roles import ADMIN
from sqlalchemy.ext.asyncio import AsyncSession
from state.admin import AdminState
from state.auth import AuthState
from state.employee import EmployeeState
from template.loader import render_template


async def start_cmd(message: Message, state: FSMContext):
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
            return await message.answer(render_template("error/user_non_active.jinja2"))

        if not user.active:
            return await message.answer(render_template("error/user_non_active.jinja2"))

        return await message.answer("Введите пароль")


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


async def check_password(message: Message, state: FSMContext):
    # async with async_db_connection() as conn:
    #     try:
    #         (user,) = (
    #             await get_user(conn, username=message.from_user.username)
    #         ).one()
    #     except NoResultFound:
    #         return await message.answer(
    #             render_template('error/password_error.jinja2')
    #         )
    #
    # if message.text != user.password:
    return await message.answer(render_template("error/password_error.jinja2"))

    # return await account_status_to_handler[user.account_status](message, state)


async def _to_admin_handlers(message: Message, state: FSMContext):
    main_buttons = ReplyKeyboardRemove()
    await state.set_state(AdminState.START)

    return await message.answer(
        "Добро пожаловать, вы вошли как администратор, воспользуйтесь меню",
        reply_markup=main_buttons,
    )


async def _to_worker_handlers(message: Message, state: FSMContext):
    main_buttons = ReplyKeyboardMarkup()
    await state.set_state(EmployeeState.START)

    return await message.answer(
        "Добро пожаловать, воспользуйтесь меню", reply_markup=main_buttons
    )


account_status_to_handler: Dict[
    str, Callable[[Message, FSMContext], Coroutine[Any, Any, Message]]
] = {"admin": _to_admin_handlers, "worker": _to_worker_handlers}


def register_handlers_auth(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands="start", state="*")
    dp.register_message_handler(check_password, state=AuthState.CHECKING_PASSWORD)
