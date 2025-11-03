from pydantic import BaseModel, ConfigDict

from app.modules.auth.domain.entities import User


class RefreshTokenQuery(BaseModel):
    user: User
    access_token: str
    refresh_token: str

    model_config = ConfigDict(arbitrary_types_allowed=True)
