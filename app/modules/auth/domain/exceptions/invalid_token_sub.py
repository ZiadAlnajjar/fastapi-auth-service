from app.modules.auth.domain.exceptions.token_exception import TokenException


class InvalidTokenSub(TokenException):
    def __init__(self):
        super().__init__()
        self.add_note("User not found or inactive.")
