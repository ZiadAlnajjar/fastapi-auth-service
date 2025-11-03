from pydantic import BaseModel


class RefreshTokenResult(BaseModel):
    access_token: str
