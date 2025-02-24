from sqlalchemy import Column, Integer, Float

from app.core.db import Base


class Wallet(Base):
    uuid = Column(Integer, nullable=False, unique=True)
    amount = Column(Float, nullable=False, default=0)
