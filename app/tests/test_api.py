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
    response = await client.get(f'{api_url}/{valid_wallet.uuid}')
    assert response.status_code == 200
    assert response.json() == {
        "id": valid_wallet.id,
        "uuid": valid_wallet.uuid,
        "balance": valid_wallet.balance
    }
