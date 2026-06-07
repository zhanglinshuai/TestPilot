
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# 创建用户时，客户端发来的json对象
class UserCreate(BaseModel):
    username: str = Field(...,min_length=1,max_length=50)
    safe_password: str = Field(...,min_length=6,max_length=72)
    email: str | None = None
    role: Literal["admin","tester","developer"] = 'tester'
# 返回给客户端的用户信息
class UserOut(BaseModel):
    id: int
    username: str
    email: str | None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # 从SQLAlchemy对象直接转换
    model_config = {"from_attributes":True}