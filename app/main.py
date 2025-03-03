from fastapi import APIRouter
from fastapi import FastAPI

from app.api.wallet import router as wallet_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description)

main_router = APIRouter(prefix=f'/api/v{settings.api_version}')
main_router.include_router(
    wallet_router,
    prefix='/wallets',
    tags=['Wallet Operations'])

app.include_router(main_router)
