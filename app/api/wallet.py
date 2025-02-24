from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.wallet import wallet_crud
from app.schemas.wallet import WalletDB

router = APIRouter()


@router.get(
    '/{WALLET_UUID}',
    response_model=WalletDB
)
async def get_wallet_balance(
        WALLET_UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await wallet_crud.get_by_uuid(WALLET_UUID, session)
