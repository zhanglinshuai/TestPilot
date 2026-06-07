from sqlalchemy.ext.asyncio import create_async_engine, async_session, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# 读取数据库url创建数据库引擎，echo=True：把每条sql打印到控制台
engine = create_async_engine(settings.database_url,echo=True)
#创建会话工厂，确保会话是异步的，并且不把对象标注为过期
async_session = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)


class Base(DeclarativeBase):
    pass

async def get_db():
    async with async_session() as session:
        try:
            # 交给调用方，等待调用方使用完后再回来执行后面的代码
            yield session
        finally:
            await session.close()