from fastapi import APIRouter

router = APIRouter()


@router.get('/{WALLET_UUID}')
async def test_app(WALLET_UUID):
    return WALLET_UUID
