from fastapi import APIRouter, Depends, status

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreateModel, UserResponseModel, UserRole

auth_router = APIRouter(tags=["auth"])


@auth_router.post(
    "/signup", summary="User signup.", status_code=status.HTTP_201_CREATED, response_model=UserResponseModel
)
async def create_user(user: UserCreateModel, db_session=Depends(get_db)):
    # validate_user_is_not_exist(cursor, user.email)
    # user_id = insert_user(db, user)
    print(user.dict())
    # try:
    new_user = User(**user.dict())  # ({"role": UserRole.AUTHORIZED, **user.dict()})
    print(new_user)
    await new_user.save(db_session)
    return new_user
    # except Exception as e:
    #     print(e, "ASDASDSA")
