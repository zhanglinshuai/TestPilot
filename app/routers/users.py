from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas.users import UserOut, UserCreate, UserLogin
from app.utils.jwt import create_access_token
from app.utils.security import hash_password
from app.utils.security import verify_password
router = APIRouter(prefix="/user", tags=["users"])


@router.post("/register", response_model=UserOut)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 检查用户名是否已经存在
    result = await db.execute(select(User).where(User.username == data.username))
    if result.scalars().first() is not None:
        raise HTTPException(status_code=409, detail="用户名已存在")
    # 把pydantic对象转为dict给model
    safed_password = hash_password(data.safe_password)
    user = User(
        username=data.username,
        safe_password=safed_password,
        email=data.email,
        role=data.role
    )
    db.add(user)  # 标记为待插入
    try:
        await db.commit()  # 提交到数据库
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="账号已存在")
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=409, detail="创建用户失败")
    await db.refresh(user)  # 从数据库重新读取这条数据
    return user  # 自动把SQLAlchemy转换为UserOut对象


@router.post("/login")
async def login_user(data: UserLogin, db: AsyncSession = Depends(get_db)):
    # 1. 查看用户是否存在
    result = await db.execute(select(User).where(User.username == data.username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=401,detail="账号或密码错误")
    # 2. 验证密码
    if not verify_password(data.safe_password, user.safe_password):
        raise HTTPException(status_code=401,detail="账号或密码错误")

    token = create_access_token(data={"sub":user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user":{
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }
@router.get("/my",response_model=UserOut)
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user

