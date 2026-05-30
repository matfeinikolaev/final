import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.models import user, category, job, vacancy, resume  # noqa: F401 - регистрируем модели

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def superuser_token(client):
    await client.post("/api/v1/auth/register", json={
        "email": "admin@test.com",
        "password": "adminpass123",
        "first_name": "Admin",
        "last_name": "User",
    })
    from sqlalchemy import select, update
    from app.models.user import User
    async with TestingSessionLocal() as session:
        await session.execute(update(User).where(User.email == "admin@test.com").values(is_superuser=True))
        await session.commit()
    resp = await client.post("/api/v1/auth/login", data={"username": "admin@test.com", "password": "adminpass123"})
    return resp.json()["access_token"]


@pytest_asyncio.fixture
async def user_token(client):
    await client.post("/api/v1/auth/register", json={
        "email": "user@test.com",
        "password": "userpass123",
        "first_name": "Regular",
        "last_name": "User",
    })
    resp = await client.post("/api/v1/auth/login", data={"username": "user@test.com", "password": "userpass123"})
    return resp.json()["access_token"]
