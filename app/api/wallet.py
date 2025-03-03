from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_wallet_exists, check_wallet_balance
from app.core.db import get_async_session
from app.crud.wallet import wallet_crud
from app.schemas.wallet import WalletDB, WalletOperation

router = APIRouter()


@router.get(
    '/{wallet_uuid}',
    response_model=WalletDB
)
async def get_wallet_balance(
        wallet_uuid,
        session: AsyncSession = Depends(get_async_session)
) -> WalletDB:
    """Получить баланс кошелька по его UUID."""
    return await check_wallet_exists(wallet_uuid, session)


@router.post(
    '/{wallet_uuid}/operation',
    response_model=WalletDB
)
async def change_wallet_balance(
        wallet_uuid,
        operation: WalletOperation = Body(
            ..., examples=WalletOperation.Config.schema_extra['examples']
        ),
        session: AsyncSession = Depends(get_async_session)
) -> WalletDB:
    """Изменить баланс кошелька (пополнение или снятие)."""
    wallet = await check_wallet_exists(wallet_uuid, session)
    operation_type = operation.operationType
    if operation_type == 'WITHDRAW':
        await check_wallet_balance(operation.amount, wallet)
    return await wallet_crud.update_balance(wallet, operation, session)


@router.post(
    '/',
    response_model=WalletDB,
)
async def create_wallet(
        session: AsyncSession = Depends(get_async_session)
):
    """Создать новый кошелёк с нулевым балансом."""
    return await wallet_crud.create(session)
