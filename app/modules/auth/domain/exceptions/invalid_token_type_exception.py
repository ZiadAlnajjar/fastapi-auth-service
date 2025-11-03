from app.modules.auth.domain.exceptions.token_exception import TokenException


class InvalidTokenTypeException(TokenException):
    def __init__(self):
        super().__init__()
