from typing import List
from fastapi import APIRouter, Body, Depends
from kubernetes.client.api.core_v1_api import CoreV1Api

from app.core.jwt import get_current_user_authorizer
from app.core.route import getMenuListByUser
from app.crud.shortcuts import check_free_email, check_free_real_name
from app.crud.user import update_user
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.kubernetes import get_k8s_core_v1_api
from app.models.user import User, UserInResponse, UserInUpdate
from app.models.route import RouteItem

router = APIRouter()


@router.get("/users/me", response_model=UserInResponse, tags=["users"])
async def retrieve_current_user(user: User = Depends(get_current_user_authorizer())):
    return UserInResponse(user=user)

@router.get("/users/menu-list", response_model=List[RouteItem], response_model_exclude_none=True, tags=["users"])
async def get_menu_list(
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api)
):
    menu = getMenuListByUser(user, core_v1_api)
    return menu

@router.put("/users", response_model=UserInResponse, tags=["users"])
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

    if(user.email):
        await check_free_email(db, user.email)
    if(user.realName):
        await check_free_real_name(db, user.realName)

    dbuser = await update_user(db, current_user.email, user)
    return UserInResponse(user=User(**dbuser.dict(), token=current_user.token))
