from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapper
from sqlalchemy.testing.schema import mapped_column

from app.database import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapper[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapper[str] = mapped_column(String(50), unique=True, nullable=False)
    safe_password: Mapper[str] = mapped_column(String(255), nullable=False)
    email: Mapper[str] = mapped_column(String(255), nullable=False)
    role: Mapper[str] = mapped_column(String(20), nullable=False, default='tester')
    is_active: Mapper[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapper[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapper[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
