import datetime as dt
import functools
from typing import Any, Callable, Dict

from fastapi import Depends, Header
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.crud import get_user
from app.schemas.user import UserResponseModel

# from app.core.exceptions import (
#     DecodeTokenException,
#     ExpiredTokenException,
#     InvalidAuthorizationTypeException,
#     NotFoundException,
# )

config = get_settings()


def _get_authorization_token(authorization: str = Header(...)) -> str:
    """Get jwt access token from header.

    Parameters
    ----------
    authorization: str
        Header where is placed Jwt access token which presents like: 'Bearer: xxxxxxxx'

    Returns
    -------
    token: str
        Jwt access token

    """
    try:
        token_prefix, token = authorization.split()

        if token_prefix != config.JWT_TOKEN_PREFIX:
            raise ValueError
    except ValueError:
        # raise InvalidAuthorizationTypeException
        raise SystemExit

    return token


async def get_current_user(
    token: str = Depends(_get_authorization_token), database: AsyncSession = Depends(get_db)
) -> UserResponseModel:
    """Get current user.

    Parameters
    ----------
    token: str
        Jwt access token

    Returns
    -------
    user: UserResponseModel
        Pydantic user model presented for viewing

    """
    payload = decode_access_token(token)
    user_email = payload["email"]
    user = await get_user(user_email, database)
    if not user:
        raise SystemExit
        # raise NotFoundException
    return user


def check_token_validness(function: Callable):
    """Validate jwt access token."""

    @functools.wraps(function)
    def _wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            # raise ExpiredTokenException
            raise SystemExit

    return _wrapper


def encode_access_token(user_email: str) -> str:
    """Create jwt access token.

    Parameters
    ----------
    user_email: str
        User email

    Returns
    -------
    str: Jwt access token (some encoded string)

    """
    payload = {
        "token_type": "access",
        "exp": dt.datetime.utcnow() + config.ACCESS_TOKEN_LIFETIME,
        "email": user_email,
    }

    return jwt.encode(payload, key=config.SECRET, algorithm=config.ALGORITHM)


@check_token_validness
def decode_access_token(access_token: str) -> Dict[str, Any]:
    """Decode jwt access token.

    Parameters
    ----------
    user_email: str
        User email

    Returns
    -------
    Dict[str, Any]: Dictionary with data from access token (for example: email)

    """
    return jwt.decode(
        access_token,
        key=config.SECRET,
        algorithms=[
            config.ALGORITHM,
        ],
    )


def encode_refresh_token(user_email: str) -> str:
    """Create jwt access token.

    Parameters
    ----------
    user_email: str
        User email

    Returns
    -------
    str: Jwt refresh token (some encoded string)

    """
    payload = {
        "token_type": "refresh",
        "exp": dt.datetime.utcnow() + config.REFRESH_TOKEN_LIFETIME,
        "email": user_email,
    }

    return jwt.encode(payload, key=config.SECRET, algorithm=config.ALGORITHM)


@check_token_validness
def decode_refresh_token(refresh_token: str) -> Dict[str, Any]:
    """Decode jwt access token.

    Parameters
    ----------
    refresh_token: str
        Jwt refresh token

    Returns
    -------
    Dict[str, Any]: Dictionary with data from refresh token (for example: email)

    """
    return jwt.decode(
        refresh_token,
        key=config.SECRET,
        algorithms=[
            config.ALGORITHM,
        ],
    )
