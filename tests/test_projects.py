import pytest
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


