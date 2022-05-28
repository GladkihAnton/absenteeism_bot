from aiogram.dispatcher.filters.state import State, StatesGroup


class WorkerState(StatesGroup):
    START = State()
