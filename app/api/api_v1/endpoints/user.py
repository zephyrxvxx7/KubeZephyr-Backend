from fastapi import APIRouter, Body, Depends

from app.core.jwt import get_current_user_authorizer
from app.crud.shortcuts import check_free_email
from app.crud.user import update_user
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.user import User, UserInResponse, UserInUpdate

router = APIRouter()


@router.get("/user", response_model=UserInResponse, tags=["users"])
async def retrieve_current_user(user: User = Depends(get_current_user_authorizer())):
    return UserInResponse(user=user)


@router.patch("/user", response_model=UserInResponse, tags=["users"])
async def update_current_user(
    user: UserInUpdate = Body(..., embed=False),
    current_user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database),
):
    if user.username == current_user.username:
        user.username = None
    if user.email == current_user.email:
        user.email = None

    await check_free_email(db, user.email)

    dbuser = await update_user(db, current_user.email, user)
    return UserInResponse(user=User(**dbuser.dict(), token=current_user.token))
