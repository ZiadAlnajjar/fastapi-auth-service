from app.core.app_base_model import AppBaseModel


class TokenPairDto(AppBaseModel):
    access_token: str
    refresh_token: str

