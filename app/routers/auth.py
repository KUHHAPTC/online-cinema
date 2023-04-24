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
    # validate_user_is_not_exist(cursor, user.email)
    # user_id = insert_user(db, user)
    # try:
    new_user = User(**user.dict())
    new_user.password = Hasher.get_password_hash(new_user.password)
    # try:
    await new_user.save(db_session)
    # except IntegrityError as no_unique_key:
    #     print("")
    return new_user
