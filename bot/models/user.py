from models.meta import DEFAULT_SCHEMA, Base
from models.office import Office
from models.role import Role
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": DEFAULT_SCHEMA}

    telegram_user_id: Column = Column(Integer, primary_key=True, index=True)

    name: Column = Column(String, nullable=False)

    role_id: Column = Column(Integer, ForeignKey(Role.id), nullable=False)
    role = relationship(Role, backref="user", uselist=False)

    office_id: Column = Column(Integer, ForeignKey(Office.id), nullable=False)
    office = relationship(Office, backref="user", uselist=False)

    absences = relationship("Absence", backref="user")

    # role = relationship(
    #     "Recipient", secondary=user_recipients, backref="customers"
    # )
