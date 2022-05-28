from typing import List

from models.absence import Absence
from sqlalchemy.sql.elements import BinaryExpression


def get_absence_filters(**kwargs) -> List[BinaryExpression]:
    filters = []
    if date := kwargs.get('date'):
        filters.append(Absence.date == date)

    if telegram_user_id := kwargs.get('telegram_user_id'):
        filters.append(Absence.telegram_user_id == telegram_user_id)

    return filters
