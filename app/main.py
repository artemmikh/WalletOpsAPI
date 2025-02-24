from fastapi import APIRouter
from fastapi import FastAPI

from app.api.wallet import router as wallet_router
from app.core.config import settings
from app.core.db import engine, Base
from app.models.wallet import Wallet  # noqa

app = FastAPI(
    title=settings.app_title,
    description=settings.description)

main_router = APIRouter(prefix=f'/api/v{settings.api_version}')
main_router.include_router(
    wallet_router,
    prefix='/wallets',
    tags=['Wallet Operations'])

app.include_router(main_router)


@app.on_event("startup")
async def on_startup():
    # временная функция до создания механизама миграций
    """Создание таблиц при старте приложения."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
