from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(prefix="/user", tags=["users"])

@router.get("/")
async def users_list(db: AsyncSession = Depends(get_db)):
    """这里先返回空数组"""
    return []