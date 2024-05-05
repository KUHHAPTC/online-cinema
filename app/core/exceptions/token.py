from .base import UnauthorizedException


class InvalidAuthorizationTypeException(UnauthorizedException):
    """Exception occur in case, if there was wrong token type in request."""

    description = "Invalid authorization token type"


class ExpiredTokenException(UnauthorizedException):
    description = "Token is expired."


class JWTTokenException(UnauthorizedException):
    description = "Invalid token representation. JWT token has to contain 3 parts separated by 2 dots."
