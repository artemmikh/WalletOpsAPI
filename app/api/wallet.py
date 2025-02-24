from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_wallet_exists
from app.core.db import get_async_session
from app.schemas.wallet import WalletDB

router = APIRouter()


@router.get(
    '/{WALLET_UUID}',
    response_model=WalletDB
)
async def get_wallet_balance(
        wallet_uuid,
        session: AsyncSession = Depends(get_async_session)
):
    wallet = await check_wallet_exists(wallet_uuid, session)
    return wallet
