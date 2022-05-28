from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminState(StatesGroup):
    START = State()
    APPROVING_CHANGING_REPORT = State()
    REPORTING_ABSENCE = State()
