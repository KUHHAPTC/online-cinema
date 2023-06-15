from fastapi import APIRouter, Depends, status

from app.core.jwt import get_current_user
from app.schemas.user import UserResponseModel

user_router = APIRouter(tags=["users"])


@user_router.get("/me", summary="User page.", status_code=status.HTTP_200_OK)  # , response_model=UserResponseModel
async def retrieve_current_user(user: UserResponseModel = Depends(get_current_user)) -> UserResponseModel:
    """Retrieve user.

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
    return UserResponseModel(**user.dict())
