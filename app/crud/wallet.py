from typing import Optional, Type, Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import Wallet


class CRUDWallet:
    """CRUD операции для модели Wallet."""

    def __init__(self, model: Type[Wallet]):
        self.model = model

    async def get_by_uuid(
            self,
            uuid: str,
            session: AsyncSession,
    ) -> Optional[Wallet]:
        """Получить кошелек по UUID."""
        wallet = await session.execute(
            select(self.model).where(
                self.model.uuid == uuid
            )
        )
        return wallet.scalars().first()

    async def update_balance(
            self,
            db_obj: Wallet,
            obj_in: Any,
            session: AsyncSession,
    ) -> Optional[Wallet]:
        """Обновить баланс кошелька."""
        try:
            stmt = select(self.model).where(
                self.model.uuid == db_obj.uuid).with_for_update()
            result = await session.execute(stmt)
            wallet = result.scalars().first()

            if not wallet:
                return None

            if obj_in.operationType == 'DEPOSIT':
                wallet.balance += obj_in.amount
            elif obj_in.operationType == 'WITHDRAW':
                wallet.balance -= obj_in.amount

            session.add(wallet)
            await session.commit()
            await session.refresh(wallet)
            return wallet
        except IntegrityError:
            await session.rollback()
            raise ValueError('Ошибка конкурентного доступа')

    async def create(
            self,
            session: AsyncSession,
    ) -> Wallet:
        """Создать новый кошелек."""
        db_obj = self.model()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


wallet_crud = CRUDWallet(Wallet)
