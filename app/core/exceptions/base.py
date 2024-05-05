import json
from enum import StrEnum
from typing import NoReturn, Type, TypeAlias

from fastapi import HTTPException, status
from sqlalchemy.exc import DBAPIError

FilePath: TypeAlias = str | None
HttpCode: TypeAlias = int


class BaseError(HTTPException):
    """Base exception class."""

    title: str
    default_detail: str
    detail: dict
    status_code: HttpCode

    def __init__(self, detail: str | None = None) -> None:
        self.detail = {
            "title": self.title,
            "detail": detail or self.default_detail,
        }

    def __str__(self) -> str:
        return json.dumps(self.detail)


class BadRequestException(BaseError):
    """
    The server cannot or will not process the request due to an apparent client error
    """

    title = "Bad Request"
    default_detail = "The server cannot process the request from the client"
    status_code = status.HTTP_400_BAD_REQUEST


class UnauthorizedException(BaseError):
    """
    The client must authenticate itself to get the requested response
    """

    title = "Unauthorized"
    default_detail = "Unauthorized"
    status_code = status.HTTP_401_UNAUTHORIZED


class ForbiddenException(BaseError):
    """
    The client does not have access rights to the content
    """

    title = "Forbidden"
    default_detail = "Forbidden"
    status_code = status.HTTP_403_FORBIDDEN


class NotFoundException(BaseError):
    """
    The server can not find the requested resource
    """

    title = "Not Found"
    default_detail = "Not Found"
    status_code = status.HTTP_404_NOT_FOUND


class RequestTimeoutException(BaseError):
    """
    The server would like to shut down this unused connection
    """

    title = "Request Timeout"
    default_detail = "Request Timeout"
    status_code = status.HTTP_408_REQUEST_TIMEOUT


class ConflictException(BaseError):
    """
    The request could not be completed due to a conflict with the current state of the resource
    """

    title = "Conflict"
    default_detail = "Some of the provided fields are already in use. Please use different values"
    status_code = status.HTTP_409_CONFLICT


class UnprocessableEntityException(BaseError):
    """
    The request was well-formed but was unable to be followed due to semantic errors
    """

    title = "Unprocessable Entity"
    default_detail = "Unprocessable Entity"
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class ServerException(BaseError):
    """
    The request could not be completed due to a server issue
    """

    title = "Internal Server Error"
    default_detail = "Internal Server Error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ForeignKeyException(UnprocessableEntityException):
    """
    The request couldn't be completed due to a ForeignKey error
    """

    default_detail = "Related entity conflict"


class DuplicatesError(BadRequestException):
    """
    The request couldn't be completed due to a DuplicatesException error
    """

    default_detail = "Duplicate error"


class NotNullViolationException(UnprocessableEntityException):
    """
    The request couldn't be completed due to a NotNullViolationException error
    """

    default_detail = "Required field is missing"


class LogicalConstraintViolationException(UnprocessableEntityException):
    """
    The request couldn't be completed due to a LogicalConstraintViolationException error
    """

    default_detail = "Logical constraint violation"


class PGErrorCodeEnum(StrEnum):
    """
    Enum for pg_code exception codes
    For more info, check the following link:
    https://github.com/MagicStack/asyncpg/blob/master/asyncpg/exceptions/__init__.py
    """

    foreign_key_violation = "23503"
    not_null_violation = "23502"
    constraint_violation = "23514"
    unique_violation = "23505"


db_error_mapping: dict[PGErrorCodeEnum, Type[BaseError]] = {
    PGErrorCodeEnum.not_null_violation: NotNullViolationException,
    PGErrorCodeEnum.constraint_violation: LogicalConstraintViolationException,
    PGErrorCodeEnum.foreign_key_violation: ForeignKeyException,
    PGErrorCodeEnum.unique_violation: ConflictException,
}


def raise_db_error(ex: DBAPIError) -> NoReturn:
    """
    Raises a more specific database error based on the given DBAPIError exception.

    :param ex: The DBAPIError exception to be handled.

    :raise: A more specific error based on the error mapping,
            or re-raises the original error if the "pgcode" is not found in the mapping.
    """

    if (error_class := db_error_mapping.get(ex.orig.pgcode)) is not None:
        exception_message: tuple[str, ...] = ex.orig.args

        errors = [error_class.default_detail, f"Error: {', '.join(exception_message)}"]

        raise error_class(". ".join(filter(None, errors)))

    raise ex
