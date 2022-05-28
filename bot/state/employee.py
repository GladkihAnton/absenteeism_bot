from aiogram.dispatcher.filters.state import State, StatesGroup


class EmployeeState(StatesGroup):
    START = State()
