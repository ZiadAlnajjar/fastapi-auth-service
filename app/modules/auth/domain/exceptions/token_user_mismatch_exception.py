from app.modules.auth.domain.exceptions.token_exception import TokenException


class TokenUserMismatchException(TokenException):
    def __init__(self):
        super().__init__()
        self.add_note("Access token sub and refresh token sub are mismatched.")
