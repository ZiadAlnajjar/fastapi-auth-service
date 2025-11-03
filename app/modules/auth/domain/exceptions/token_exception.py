class TokenException(Exception):
    def __init__(self, detail="Invalid or expired token."):
        super().__init__(detail)
