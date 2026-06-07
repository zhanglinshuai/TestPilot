from fastapi import APIRouter,HTTPException,Depends
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User
from app.schemas.users import UserOut, UserCreate
from app.utils.security import hash_password

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/")
async def users_list(db: AsyncSession = Depends(get_db)):
    """这里先返回空数组"""
    return []


@router.post("/create", response_model=UserOut)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    #检查用户名是否已经存在
    result = await db.execute(select(User).where(User.username==data.username))
    if result.scalars().first() is not None:
        raise HTTPException(status_code=409,detail="用户名已存在")
    # 把pydantic对象转为dict给model
    safed_password = hash_password(data.safe_password)
    user = User(
        username=data.username,
        safe_password=safed_password,
        email=data.email,
        role=data.role
    )
    db.add(user) # 标记为待插入
    try:
        await db.commit() # 提交到数据库
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409,detail="用户名已存在")
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=409,detail="创建用户失败")
    await db.refresh(user) # 从数据库重新读取这条数据
    return user  #自动把SQLAlchemy转换为UserOut对象
