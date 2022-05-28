from typing import List

from models.role import Role
from models.user import User
from sqlalchemy.sql.elements import BinaryExpression


def get_user_filters(**kwargs) -> List[BinaryExpression]:
    filters = []
    if user_id := kwargs.get('telegram_user_id'):
        filters.append(User.telegram_user_id == user_id)

    if role := kwargs.get('role'):
        filters.append(Role.name == role)

    return filters
