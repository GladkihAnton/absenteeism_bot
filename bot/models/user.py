from models.meta import DEFAULT_SCHEMA, Base
from models.office import Office
from models.role import Role
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": DEFAULT_SCHEMA}

    telegram_user_id: Column = Column(Integer, primary_key=True, index=True)

    name: Column = Column(String, nullable=False)
    active: Column = Column(Boolean, default=False, nullable=False)

    role = relationship(Role, backref="user", uselist=False)
    role_id: Column = Column(Integer, ForeignKey(Role.id), nullable=False)

    office = relationship(Office, backref="user", uselist=False)
    office_id: Column = Column(Integer, ForeignKey(Office.id), nullable=False)

    absences = relationship("Absence", backref="user")
