from typing import Any, Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserResponseModel


def get_user_as_dict(user: User) -> Dict[str, Any]:
    """Get user sqlalchemy model as dict.

    Parameters
    ----------
    user: User
        Sqlalchemy model for user

    Returns
    -------
    Dict[str, Any]: User model from db but presented as dict

    """
    return user.__dict__


async def get_user(email: str, database: AsyncSession) -> UserResponseModel | None:
    """Get user pydantic response model.

    Parameters
    ----------
    email: str
        User email
    db_session: AsyncSession
        Asynchronous connection to database

    Returns
    -------
    user_data: UserResponseModel | None
        Pydantic user model presented for viewing

    """
    user_item = await database.execute(select(User).where(User.email == email))
    user_data = result[0] if (result := user_item.fetchone()) else None
    if user_data:
        return UserResponseModel(**get_user_as_dict(user_data))
    return None
