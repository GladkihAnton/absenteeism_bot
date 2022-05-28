from typing import Callable, Dict, Coroutine, Any

from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from db import async_db_connection
from sqlalchemy.exc import NoResultFound

from state.auth import AuthState
from state.admin import AdminState
from state.worker import WorkerState
from template.loader import render_template


class AuthMiddleware(BaseMiddleware):
    async def on_process_message(self, message: Message, data):
        state: FSMContext = data['state']
        if not await state.get_state() and message.get_command() not in ['/start']:
            await message.answer(
                'Воспользуйтесь командой /start', reply_markup=ReplyKeyboardRemove()
            )
            raise CancelHandler()


async def start_cmd(message: Message, state: FSMContext):
    await state.set_state(AuthState.CHECKING_PASSWORD)
    return await message.answer('Введите пароль')


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
    return await message.answer(
        render_template('error/password_error.jinja2')
    )

    # return await account_status_to_handler[user.account_status](message, state)


async def _to_admin_handlers(message: Message, state: FSMContext):
    main_buttons = ReplyKeyboardRemove()
    await state.set_state(AdminState.START)

    return await message.answer(
        'Добро пожаловать, вы вошли как администратор, воспользуйтесь меню', reply_markup=main_buttons
    )


async def _to_worker_handlers(message: Message, state: FSMContext):
    main_buttons = ReplyKeyboardMarkup()
    await state.set_state(WorkerState.START)

    return await message.answer(
        'Добро пожаловать, воспользуйтесь меню', reply_markup=main_buttons
    )


account_status_to_handler: Dict[str, Callable[[Message, FSMContext], Coroutine[Any, Any, Message]]] = {
    'admin': _to_admin_handlers,
    'worker': _to_worker_handlers
}


def register_handlers_auth(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands="start", state="*")
    dp.register_message_handler(check_password, state=AuthState.CHECKING_PASSWORD)
