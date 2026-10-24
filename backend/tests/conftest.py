import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.mongodb import db_manager
from scripts.seed_data import seed_database


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_database():
    """Ensure mock database is connected and seeded for test suite."""
    db_manager.connect(force_mock=True)
    seed_database(auto_if_empty=False)
    yield
    db_manager.disconnect()


@pytest_asyncio.fixture
async def client():
    """Asynchronous HTTP test client bound to FastAPI application."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver/api/v1") as ac:
        yield ac
