from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.wallet import wallet_crud
from app.models.wallet import Wallet


async def check_wallet_exists(
        wallet_uuid: int,
        session: AsyncSession,
) -> Optional[Wallet]:
    wallet: Optional[Wallet] = await wallet_crud.get_by_uuid(
        wallet_uuid, session)
    if wallet is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Кошелёк не найден!'
        )
    return wallet


async def check_wallet_balance(amount: float, wallet: Wallet):
    wallet_balance = wallet.balance
    if wallet_balance - amount < 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Не хватает средств для снятия. '
                   f'Баланс кошелька: {wallet_balance}'
        )
