from fastapi import APIRouter, Body, Depends

from app.core.jwt import get_current_user_authorizer
from app.crud.shortcuts import check_free_email
from app.crud.user import update_user
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.user import User, UserInResponse, UserInUpdate

router = APIRouter()


@router.get("/users/me", response_model=UserInResponse, tags=["users"])
async def retrieve_current_user(user: User = Depends(get_current_user_authorizer())):
    return UserInResponse(user=user)


@router.put("/user", response_model=UserInResponse, tags=["users"])
async def update_current_user(
    user: UserInUpdate = Body(..., embed=False),
    current_user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database),
):
    if user.email == current_user.email:
        user.email = None
    if user.realName == current_user.realName:
        user.realName = None
    if user.desc == current_user.desc:
        user.desc = None

    await check_free_email(db, user.email)

    dbuser = await update_user(db, current_user.email, user)
    return UserInResponse(user=User(**dbuser.dict(), token=current_user.token))
