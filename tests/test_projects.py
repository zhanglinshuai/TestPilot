import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.database import Base, get_db
from app.main import app

# 模拟测试数据库，不适用真实的db防止污染数据
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def setup_db():
    """每次测试前建表。用完后销毁"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# 替换数据库依赖
async def override_get_db():
    async with TestSession() as session:
        yield session


# 不再调用原来的get_db而是调用override_get_db
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# 完成注册登录功能，获取token
async def get_token(async_client) -> str:
    await async_client.post("/user/register", json={
        "username": "tester1",
        "safe_password": "123456",
        "role": "tester"
    })
    response = await async_client.post("/user/login", json={
        "username": "tester1",
        "safe_password": "123456"
    })
    return response.json()["access_token"]


# 测试创建项目功能
@pytest.mark.asyncio
async def test_create_project_access(async_client):
    token = await get_token(async_client)
    response = await async_client.post("/project/create", json={
        "name": "testPilot",
        "repo_url": "https://github.com/testPilot",
        "description": "testPilot",
        "default_env_id": 100,
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, f"失败详情:{response.json()}"
    data = response.json()
    assert data["name"] == "testPilot"
    assert data["is_active"] is True
