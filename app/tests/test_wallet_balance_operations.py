from http import HTTPStatus

import pytest
from httpx import AsyncClient

from app.models.wallet import Wallet


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'operation_type, amount, expected_balance, expected_status',
    [
        ('WITHDRAW', 1, lambda balance: balance - 1, HTTPStatus.OK),
        ('DEPOSIT', 1, lambda balance: balance + 1, HTTPStatus.OK),
        ('WITHDRAW', 1000, lambda balance: balance, HTTPStatus.BAD_REQUEST),
    ]
)
async def test_wallet_operation(
        api_url: str,
        client: AsyncClient,
        test_wallet,
        valid_wallet: Wallet,
        operation_type,
        amount,
        expected_balance,
        expected_status
):
    """Тест на пополнение и снятие средств с кошелька."""
    response = await client.post(
        f'{api_url}/{valid_wallet.uuid}/operation',
        json={"operationType": operation_type, "amount": amount}
    )

    assert response.status_code == expected_status

    if expected_status == HTTPStatus.OK:
        assert response.json() == {
            "id": valid_wallet.id,
            "uuid": valid_wallet.uuid,
            "balance": expected_balance(valid_wallet.balance)
        }
    elif expected_status == HTTPStatus.BAD_REQUEST:
        assert response.json() == {
            "detail": f'Не хватает средств для снятия. '
                      f'Баланс кошелька: {valid_wallet.balance}'
        }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'operation_type',
    ['WITHDRAW', 'DEPOSIT']
)
async def test_wallet_not_found(
        api_url: str,
        client: AsyncClient,
        operation_type
):
    """Тест на операции с несуществующим кошельком."""
    response = await client.post(
        f'{api_url}/00000000-0000-0000-0000-000000000000/operation',
        json={"operationType": operation_type, "amount": 1}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Кошелёк не найден!"}
