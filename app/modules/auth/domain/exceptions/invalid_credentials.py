from app.domain.exceptions.base import DomainException


class InvalidCredentials(DomainException):
    def __init__(self, detail="Invalid email or password"):
        super().__init__(detail)
