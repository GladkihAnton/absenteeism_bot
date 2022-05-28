from models.meta import DEFAULT_SCHEMA, Base
from models.user import User
from sqlalchemy import Column, Date, ForeignKey, Integer, String


class Absence(Base):
    __tablename__ = "absence"
    __table_args__ = {"schema": DEFAULT_SCHEMA}

    id: Column = Column(Integer, primary_key=True, index=True)

    message: Column = Column(String, nullable=False)
    date: Column = Column(Date, nullable=False)

    telegram_user_id: Column = Column(
        String, ForeignKey(User.telegram_user_id), nullable=False
    )
