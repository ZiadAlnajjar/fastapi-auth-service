from app.core.app_base_model import AppBaseModel
from app.modules.auth.application.commands.register_user.register_user_result import RegisterUserResult


class RegisterUserResponse(AppBaseModel, RegisterUserResult):
    pass
