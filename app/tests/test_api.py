import pytest
from httpx import AsyncClient

from app.models.wallet import Wallet


@pytest.mark.asyncio
async def test_wallet_balance(
        api_url: str,
        client: AsyncClient,
        test_wallet,
        valid_wallet: Wallet
):
    """Тест на получение баланса существующего кошелька."""
    response = await client.get(f'{api_url}/{valid_wallet.uuid}')
    assert response.status_code == 200
    assert response.json() == {
        "id": valid_wallet.id,
        "uuid": valid_wallet.uuid,
        "balance": valid_wallet.balance
    }


@pytest.mark.asyncio
async def test_wallet_balance_not_found(
        api_url: str,
        client: AsyncClient
):
    """Тест на получение баланса несуществующего кошелька."""
    non_existent_uuid = '00000000-0000-0000-0000-000000000000'
    response = await client.get(f'{api_url}/{non_existent_uuid}')
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Кошелёк не найден!"
    }
