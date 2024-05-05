from .base import ConflictException, UnauthorizedException


class UserExistsException(ConflictException):
    def __init__(self, email: str) -> None:
        detail = f"User with email '{email}' already exists"
        super().__init__(detail=detail)


class InvalidCredentialsException(UnauthorizedException):
    description = "Provided credentials are invalid"
