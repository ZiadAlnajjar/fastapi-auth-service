from app.modules.auth.domain.entities.user import User
from .register_user_command import RegisterUserCommand
from .register_user_result import RegisterUserResult
from ...dtos.user_dto import UserDto


class RegisterUserMapper:
    @staticmethod
    def to_entity(command: RegisterUserCommand, hashed_password: str) -> User:
        return User(
            email=str(command.email),
            username=command.username,
            hashed_password=hashed_password,
        )

    @staticmethod
    def to_result(user: User) -> RegisterUserResult:
        user_dto = UserDto.from_entity(user)
        return RegisterUserResult(
            id=user_dto.id,
            email=user_dto.email,
            username=user_dto.username,
            role=user_dto.role,
            is_active=user_dto.is_active,
            created_at=user_dto.created_at,
        )
