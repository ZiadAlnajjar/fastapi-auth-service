from app.domain.exceptions.not_found_exception import NotFoundException


class UserNotFoundException(NotFoundException):
    def __init__(self, field: str, value: str):
        super().__init__("User", field, value)
