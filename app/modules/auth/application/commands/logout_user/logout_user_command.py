from typing import Optional

from app.core.app_base_model import AppBaseModel


class LogoutUserCommand(AppBaseModel):
    access_token: str
    refresh_token: Optional[str] = None
