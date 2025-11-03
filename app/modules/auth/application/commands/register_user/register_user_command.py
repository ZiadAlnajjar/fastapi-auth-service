from pydantic import EmailStr, Field

from app.core.app_base_model import AppBaseModel


class RegisterUserCommand(AppBaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=8, max_length=64)
