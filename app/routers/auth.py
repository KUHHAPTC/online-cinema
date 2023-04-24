from fastapi import APIRouter, Depends, status

from app.core.database import get_db
from app.core.security import Hasher
from app.models.user import User
from app.schemas.user import UserCreateModel, UserResponseModel

auth_router = APIRouter(tags=["auth"])


@auth_router.post(
    "/signup", summary="User signup.", status_code=status.HTTP_201_CREATED, response_model=UserResponseModel
)
async def create_user(user: UserCreateModel, db_session=Depends(get_db)):
    """Create new user.

    Parameters
    ----------
    user: UserCreateModel
        Pydantic model for user creation
    db_session: AsyncSession
        Asynchronous connection to database

    Returns
    -------
    new_user: UserResponseModel
        Pydantic model with neccessary field

    """
    new_user = User(**user.dict())
    new_user.password = Hasher.get_password_hash(new_user.password)
    await new_user.save(db_session)
    return new_user
