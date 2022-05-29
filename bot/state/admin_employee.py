from aiogram.dispatcher.filters.state import State, StatesGroup


class BaseAdminEmployeeState(StatesGroup):
    START = State()
    APPROVING_CHANGING_REPORT = State()
    REPORTING_ABSENCE = State()
