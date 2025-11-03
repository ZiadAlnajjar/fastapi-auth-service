from app.core.app_base_model import AppBaseModel
from app.modules.auth.application.commands.refresh_token.refresh_token_result import RefreshTokenResult


class RefreshTokenResponse(AppBaseModel, RefreshTokenResult):
    pass
