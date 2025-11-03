from pydantic import BaseModel


class LoginUserResult(BaseModel):
    access_token: str
    refresh_token: str
    token_type_hint: str
