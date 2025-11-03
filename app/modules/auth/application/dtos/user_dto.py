from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.modules.auth.domain.entities.user import User


class UserDto(BaseModel):
    id: str
    email: EmailStr
    username: str
    role: str
    is_active: bool
    created_at: datetime

    @staticmethod
    def from_entity(user: User) -> "UserDto":
        return UserDto(
            id=user.public_id,
            email=user.email,
            username=user.username,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
        )
