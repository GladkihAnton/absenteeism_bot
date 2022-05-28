from models.meta import DEFAULT_SCHEMA, Base
from sqlalchemy import Column, Integer, String


class Office(Base):
    __tablename__ = "office"
    __table_args__ = {"schema": DEFAULT_SCHEMA}

    id: Column = Column(Integer, primary_key=True, index=True)

    name: Column = Column(String, nullable=False)
