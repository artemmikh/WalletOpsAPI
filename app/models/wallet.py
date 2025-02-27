import uuid

from sqlalchemy import Column, String, Float

from app.core.db import Base


class Wallet(Base):
    """Модель кошелька."""
    uuid = Column(
        String(36),
        default=lambda: str(uuid.uuid4()))
    balance = Column(
        Float,
        nullable=False,
        default=0)
