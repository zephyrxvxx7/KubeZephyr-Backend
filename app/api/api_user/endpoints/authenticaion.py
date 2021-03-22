from datetime import timedelta

from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from kubernetes import client

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.jwt import create_access_token
from app.crud.shortcuts import check_free_email
from app.crud.user import create_user, get_user_by_email
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.user import User, UserInCreate, UserInLogin, UserInResponse
from app.kubernetes import get_k8s_core_v1_api, get_k8s_storage_v1_api

router = APIRouter()

@router.post("/users/login", response_model=UserInResponse, tags=["authentication"])
async def login(
        user: UserInLogin = Body(..., embed=False), db: AsyncIOMotorClient = Depends(get_database)
):
    dbuser = await get_user_by_email(db, user.email)
    if not dbuser or not dbuser.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"email": dbuser.email}, expires_delta=access_token_expires
    )
    return UserInResponse(user=User(**dbuser.dict(), token=token))


@router.post(
    "/users",
    response_model=UserInResponse,
    tags=["authentication"],
    status_code=HTTP_201_CREATED,
)
async def register(
        user: UserInCreate = Body(..., embed=False), 
        db: AsyncIOMotorClient = Depends(get_database), 
        core_v1_api = Depends(get_k8s_core_v1_api), 
        storage_v1_api = Depends(get_k8s_storage_v1_api)
):
    await check_free_email(db, user.email)

    async with await db.start_session() as s:
        async with s.start_transaction():
            dbuser = await create_user(db, user, core_v1_api, storage_v1_api)
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            token = create_access_token(
                # data={"username": dbuser.username}, expires_delta=access_token_expires
                data={"email": dbuser.email}, expires_delta=access_token_expires
            )

    return UserInResponse(user=User(**dbuser.dict(), token=token))
