from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi.responses import Response
from kubernetes.client.api.core_v1_api import CoreV1Api

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.core.jwt import get_current_user_authorizer
from app.core.permission import check_permission_with_exception
from app.crud.user import crud_get_many_user, delete_user, get_user_by_user_id
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.user import ManyUserInResponse, ManyUser, User
from app.models.route import RoleEnum
from app.models.rwmodel import OID

from app.kubernetes import get_k8s_core_v1_api
from app.kubernetes.namespace import delete_namespace

router = APIRouter()

@router.get(
    "/users",
    response_model=ManyUserInResponse,
    tags=["ADMIN users"]
)
async def get_users(
    current_user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    check_permission_with_exception(current_user.roles, RoleEnum.SUPER)

    dbuser = await crud_get_many_user(db)

    if not dbuser:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Any user not found"
        )

    return ManyUserInResponse(user=[ManyUser(**user.dict()) for user in dbuser])

@router.delete(
    "/users/{user_id}", 
    tags=["ADMIN users"],
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_user_by_user_id(
    user_id: OID = Path(...),
    current_user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api)
):
    check_permission_with_exception(current_user.roles, RoleEnum.SUPER)

    if not await get_user_by_user_id(db, user_id):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"User with the user id is not founded"
        )

    await delete_user(db, user_id)
    delete_namespace(core_v1_api, str(user_id))

    return Response(status_code=HTTP_204_NO_CONTENT)