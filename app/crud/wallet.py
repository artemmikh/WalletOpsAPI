from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import Wallet


class CRUDWallet:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_by_uuid(
            self,
            uuid: int,
            session: AsyncSession,
    ):
        wallet = await session.execute(
            select(self.model).where(
                self.model.uuid == uuid
            )
        )
        return wallet.scalars().first()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update_balance(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
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


wallet_crud = CRUDWallet(Wallet)
