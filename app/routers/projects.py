from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Project, User
from app.routers.users import get_current_user
from app.schemas.projects import ProjectOut, ProjectCreate, ProjectUpdate

router = APIRouter(prefix="/project", tags=["projects"])


# 创建项目方法
@router.post("/create", response_model=ProjectOut)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    # 检查项目名是否存在。存在的话不允许创建
    result = await db.execute(select(Project).where(Project.name == data.name))
    # 如果不为空说明存在
    if result.scalars().first() is not None:
        raise HTTPException(status_code=419, detail="项目已存在")
    # 把pydantic对象转为dict给Model
    project = Project(
        name=data.name,
        description=data.description,
        repo_url=data.repo_url,
        default_env_id=data.default_env_id,
    )
    # 将数据标记为待插入
    db.add(project)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=419, detail="项目已存在")
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=419, detail="创建项目失败")
    await db.refresh(project)  # 从数据库中读取这条数据
    return project  # 自动把SQLAlchemy转换为ProjectOut对象



def check_project_permission(project: Project, current_user:User):
    """校验用户编辑和删除权限，目前只给创建者或者admin开放"""
    if current_user.id!=project.created_by or current_user.role!= "admin":
        raise HTTPException(status_code=403,detail="无权限，仅项目创建者或管理员可操作")

# 编辑项目
@router.post("/update", response_model=ProjectOut)
async def update_project(
        project_id: int,
        data: ProjectUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # 判断项目是否存在
    result = await db.execute(select(Project).where(Project.id == data.id))
    project = result.scalars().first()
    # 项目不存在
    if project is None:
        raise HTTPException(status_code=419, detail="项目不存在")
    # 校验当前用户的权限
    check_project_permission(project,current_user)
    # 提取客户端传了的字段
    update_data = data.model_dump(exclude_unset=True)
    # 如果传了name，需要检查传之后的name是否和之前的项目重名
    if "name" in update_data:
        dup = await db.execute(select(Project).where(
            Project.name == update_data["name"],
            Project.id != project_id,
        )
    )
        if dup.scalars().first():
            raise HTTPException(status_code=419,detail="项目名称已存在")
    # 给客户端传了的字段赋值
    for field,value in update_data.items():
        setattr(project, field, value)
    # 注入修改人的值
    project.updated_by = current_user.id
    await db.commit()
    await db.refresh(project)
    return project
