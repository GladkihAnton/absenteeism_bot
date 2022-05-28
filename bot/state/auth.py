from aiogram.dispatcher.filters.state import State, StatesGroup


class AuthState(StatesGroup):
    CHECKING_PASSWORD = State()
