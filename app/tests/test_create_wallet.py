from http import HTTPStatus
from uuid import UUID

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_wallet(
        api_url: str,
        client: AsyncClient,
):
    """Тест на создание кошелька."""
    response = await client.post(f'{api_url}/')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()

    assert 'id' in response_data
    assert 'uuid' in response_data
    assert 'balance' in response_data

    assert isinstance(response_data['id'], int)
    try:
        UUID(response_data['uuid'])
    except ValueError:
        pytest.fail('Не валидный uuid')
    assert response_data['balance'] == 0.0
