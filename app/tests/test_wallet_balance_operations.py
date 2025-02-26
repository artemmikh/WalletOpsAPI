from http import HTTPStatus

import pytest
from httpx import AsyncClient

from app.models.wallet import Wallet


@pytest.mark.asyncio
async def test_withdraw_wallet(
        api_url: str,
        client: AsyncClient,
        test_wallet,
        valid_wallet: Wallet
):
    """Тест на снятие средств существующего кошелька."""
    response = await client.post(
        f'{api_url}/{valid_wallet.uuid}/operation',
        json={
            "operationType": "WITHDRAW",
            "amount": 1
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": valid_wallet.id,
        "uuid": valid_wallet.uuid,
        "balance": valid_wallet.balance - 1
    }


@pytest.mark.asyncio
async def test_withdraw_wallet_not_found(
        api_url: str,
        client: AsyncClient,
        test_wallet,
        valid_wallet: Wallet
):
    """Тест на снятие средств не существующего кошелька."""
    response = await client.post(
        f'{api_url}/{"00000000-0000-0000-0000-000000000000"}/operation',
        json={
            "operationType": "WITHDRAW",
            "amount": 1
        }
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "detail": "Кошелёк не найден!"
    }
