import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.database import Base, get_db
from app.main import app

# 模拟测试数据库，不适用真实的db防止污染数据
TEST_DATABASE_URL="sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSession = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)

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
app.dependency_overrides[get_db]=override_get_db

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url="http://test") as client:
        yield client

#测试登录功能正常使用
@pytest.mark.asyncio
async def test_create_user_success(async_client):
    response = await async_client.post("/user/create",json={
        "username":"linshuai",
        "safe_password":"123456",
        "email":"zhanglinshuai01@gmail.com",
        "role":"admin"
    })
    assert response.status_code == 200
    user =  response.json()
    assert user["username"] == "linshuai"
    assert user["email"] =="zhanglinshuai01@gmail.com"
    assert user["role"] == "admin"
    assert user["is_active"] is True
    assert "safe_password" not in user


#测试登录名不能相同
@pytest.mark.asyncio
async def test_create_user_same_name(async_client):
    await async_client.post("/user/create",json={
        "username":"linshuai",
        "safe_password":"123456",
        "email":"zhanglinshuai01@gmail.com",
        "role":"admin"
    })
    same_user = await async_client.post("/user/create", json={
        "username": "linshuai",
        "safe_password": "654321",
        "email": "zhanglinshuai01@gmail.com",
        "role": "admin"
    })
    assert same_user.status_code == 409
    assert '已存在' in same_user.json()['detail']

#测试校验密码
@pytest.mark.asyncio
async def test_create_user_missing_password(async_client):
    response = await async_client.post("/user/create",json={
        "username":"linshuai",
        "role": "admin"
    })
    assert response.status_code == 422 #Pydantic校验失败

#测试角色范围
@pytest.mark.asyncio
async def test_create_user_role_range(async_client):
    response = await async_client.post("/user/create",json={
        "username":"linshuai",
        "safe_password":"123456",
        "role":"123456"
    })

    assert response.status_code == 422
