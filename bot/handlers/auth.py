from typing import Any, Callable, Coroutine, Dict

from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from crud.filters.user import get_user_filters
from crud.user import get_user
from db import async_db_connection
from state.admin import AdminState
from state.auth import AuthState
from state.employee import EmployeeState
from template.loader import render_template


async def start_cmd(message: Message, state: FSMContext):
    filters = get_user_filters(user_id=message.chat.id)
    async with async_db_connection() as conn:
        user = (await get_user(conn, filters)).scalar()
    # x = 1
    # a = message.bot.get_chat_member(message.from_user.id, message.chat.id)
    # if not user:
    await state.set_state(AuthState.CHECKING_PASSWORD)
    return await message.answer("Введите пароль")


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
