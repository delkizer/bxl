class BaseProjectError(Exception):
    def __init__(self, message=None, status_code=500):
        super().__init__(message or "BaseProjectError")
        self.message = message or "BaseProjectError"
        self.status_code = status_code

class PrivateKeyNotFoundError(BaseProjectError):
    def __init__(self, message="Private key file not found", status_code=404):
        super().__init__(message, status_code)

class ExpiredTokenError(BaseProjectError):
    def __init__(self, message="Token expired", status_code=401):
        super().__init__(message, status_code)

class InvalidTokenError(BaseProjectError):
    def __init__(self, message="Invalid token", status_code=401):
        super().__init__(message, status_code)

