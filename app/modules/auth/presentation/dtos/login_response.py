from app.core.app_base_model import AppBaseModel
from app.modules.auth.application.queires.login_user.login_user_result import LoginUserResult


class LoginResponse(AppBaseModel, LoginUserResult):
    pass
