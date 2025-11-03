from pydantic import EmailStr
from app.core.app_base_model import AppBaseModel


class LoginUserQuery(AppBaseModel):
    email: EmailStr
    password: str
