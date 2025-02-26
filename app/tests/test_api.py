import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_wallet_balance(api_url, client: AsyncClient):
    response = await client.get(f'/{api_url}/wallets/1')
    assert response.status_code == 200
