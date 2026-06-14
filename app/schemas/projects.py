from datetime import datetime

from pydantic import BaseModel, Field


# 客户端创建项目字段
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = Field(None, max_length=500)
    repo_url: str = Field(...,min_length=1,max_length=500)
    default_env_id : int= Field(ge=1)
# 客户端更新项目字段
class ProjectUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(..., min_length=0, max_length=500)
    repo_url: str = Field(..., min_length=1, max_length=500)
    default_env_id: int = Field(ge=1)
    is_active: bool
# 客户端返回项目的字段
class ProjectOut(BaseModel):
    id: int
    name:str
    description: str | None
    repo_url: str
    default_env_id: int
    created_by: int
    updated_by: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
# 客户端删除项目字段
class ProjectDelete(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
