from app.modules.auth.domain.exceptions.token_exception import TokenException


class RevokedTokenException(TokenException):
    def __init__(self):
        super().__init__()
        self.add_note("Token has been blacklisted")
