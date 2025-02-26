import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.core.config import settings
from app.main import app


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def api_url() -> str:
    return f'api/v{settings.api_version}'
