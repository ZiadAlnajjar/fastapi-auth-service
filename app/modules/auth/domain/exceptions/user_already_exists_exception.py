from app.domain.exceptions.already_exists_exception import AlreadyExistsException


class UserAlreadyExists(AlreadyExistsException):
    def __init__(self, field: str, value: str):
        super().__init__("User", field, value)
