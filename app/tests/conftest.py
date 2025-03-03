import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.db import Base, get_async_session
from app.main import app
from app.models.wallet import Wallet


@pytest_asyncio.fixture
async def test_db():
    """Создаёт временную БД и удаляет после тестов."""
    engine = create_async_engine(settings.test_database_url, echo=True)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_session_maker

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def override_get_async_session(test_db):
    """Заменяет сессию БД в приложении на тестовую."""

    async def _get_test_session():
        async with test_db() as session:
            yield session

    app.dependency_overrides[get_async_session] = _get_test_session
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def valid_wallet() -> Wallet:
    """Создаёт и возвращает валидный экземпляр класса "Wallet"."""
    return Wallet(
        id=1,
        uuid='550e8400-e29b-41d4-a716-446655440000',
        balance=100.0
    )


@pytest_asyncio.fixture
async def test_wallet(test_db, valid_wallet):
    """Добавляет тестовые данные в тестовую базу."""
    async with test_db() as session:
        session.add(valid_wallet)
        await session.commit()
        await session.refresh(valid_wallet)
        return valid_wallet


@pytest_asyncio.fixture
async def client(override_get_async_session) -> AsyncClient:
    """Создает и возвращает клиент, который использует тестовую БД."""
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def api_url() -> str:
    """Возвращает путь к api кошельков."""
    return f'api/v{settings.api_version}/wallets'
