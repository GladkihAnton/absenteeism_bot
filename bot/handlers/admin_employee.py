from datetime import date

from action.common import REPORT_ABSENCE, ActionData, \
    APPROVED_OR_NOT_CHANGING_REPORT
from crud.absence import get_absence, create_absence
from crud.filters.absence import get_absence_filters

from db import async_db_connection
from models import Absence

from typing import Optional, Dict

from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from state.admin_employee import BaseAdminEmployeeState
from template.loader import render_template


async def on_try_report_absence(message: Message, state: FSMContext):
    async with async_db_connection() as conn:
        filters = get_absence_filters(telegram_user_id=message.from_user.id, date=date.today())
        absence: Optional[Absence] = (await get_absence(conn, filters)).scalar()

    if not absence:
        await state.set_state(BaseAdminEmployeeState.REPORTING_ABSENCE)
        return await message.answer(render_template('report_absence.jinja2', date=date.today()))

    await state.set_state(BaseAdminEmployeeState.APPROVING_CHANGING_REPORT)
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text='Да',
            callback_data=ActionData.new(action=APPROVED_OR_NOT_CHANGING_REPORT,
                                         value='approve')
        ),
        InlineKeyboardButton(
            text='Нет',
            callback_data=ActionData.new(action=APPROVED_OR_NOT_CHANGING_REPORT,
                                         value='dont_approve'),
        ),
    )
    return await message.answer(
        render_template('do_change_report.jinja2', message=absence.message),
        reply_markup=keyboard)


async def on_report_absence(message: Message, state: FSMContext):
    async with async_db_connection() as conn:
        await create_absence(conn, date=date.today(),
                             message=message.text,
                             telegram_user_id=message.from_user.id)
        await conn.commit()

    await state.set_state(BaseAdminEmployeeState.START)
    return await message.answer(render_template('to_start.jinja2'))


async def on_approve_changing_absence(call: CallbackQuery, state: FSMContext, callback_data: Dict):
    match callback_data['value']:
        case 'approve':
            await state.set_state(BaseAdminEmployeeState.REPORTING_ABSENCE)
            return await call.message.answer(render_template('report_absence.jinja2', date=date.today()))
        case 'dont_approve':
            await state.set_state(BaseAdminEmployeeState.START)
            return await call.message.answer(render_template('to_start.jinja2'))
        case _:
            await state.set_state(BaseAdminEmployeeState.START)
            return await call.message.answer(render_template('unexpected_behaviour.jinja2'))


def register_handlers_admin_employee(dp: Dispatcher):
    dp.register_message_handler(on_try_report_absence,
                                lambda message: message.text == REPORT_ABSENCE,
                                state=BaseAdminEmployeeState.states)
    dp.register_message_handler(on_report_absence, state=BaseAdminEmployeeState.REPORTING_ABSENCE)
    dp.register_callback_query_handler(
        on_approve_changing_absence,
        ActionData.filter(action=APPROVED_OR_NOT_CHANGING_REPORT),
        state=BaseAdminEmployeeState.APPROVING_CHANGING_REPORT,
    )
