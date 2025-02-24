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
