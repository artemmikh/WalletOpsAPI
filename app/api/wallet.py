from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_wallet_exists, check_wallet_balance
from app.core.db import get_async_session
from app.schemas.wallet import WalletDB, WalletOperation

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


@router.post(
    '/{WALLET_UUID}/operation',
    # response_model=WalletDB
)
async def change_wallet_balance(
        wallet_uuid,
        operation: WalletOperation = Body(
            ..., examples=WalletOperation.Config.schema_extra['examples']
        ),
        session: AsyncSession = Depends(get_async_session)
):
    wallet = await check_wallet_exists(wallet_uuid, session)
    if operation.operationType == 'WITHDRAW':
        await check_wallet_balance(operation.amount, wallet)
