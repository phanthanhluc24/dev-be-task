class AppException(Exception):
    """Base for all custom app exceptions."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)


class ConflictException(AppException):
    def __init__(self, message="Resource already exists"):
        super().__init__(message, status_code=409)


class BadRequestException(AppException):
    def __init__(self, message="Bad request"):
        super().__init__(message, status_code=400)


class UnauthorizedException(AppException):
    def __init__(self, message="Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenException(AppException):
    def __init__(self, message="Forbidden"):
        super().__init__(message, status_code=403)
