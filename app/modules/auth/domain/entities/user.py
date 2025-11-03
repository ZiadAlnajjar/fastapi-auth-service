from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, Boolean, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base
from app.infrastructure.database.mixins import SoftDeleteMixin


class User(Base, SoftDeleteMixin):
    id = Base.id
    public_id: Mapped[str] = mapped_column(UUID, default=lambda: str(uuid4()), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String(50), default='user')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
