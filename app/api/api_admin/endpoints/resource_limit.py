from fastapi import APIRouter, Body, Depends, Path, HTTPException

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.core.jwt import get_current_user_authorizer
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.resource_limit import (
    ResourceLimitBase,
    ResourceLimitInCreate,
    ResourceLimitInResponse,
    ResourceLimitInUpdate
)
from app.crud.resource_limit import (
    crud_create_limit_by_id,
    crud_get_limit_by_id,
    crud_update_limit_by_id
)
from app.models.rwmodel import OID

router = APIRouter()

@router.post("/resources/limit",
    response_model=ResourceLimitInResponse,
    tags=["ADMIN Resources Limit"],
    status_code=HTTP_201_CREATED
)
async def create_resource_limit(
        resource_limit: ResourceLimitInCreate = Body(..., embed=False),
        db: AsyncIOMotorClient = Depends(get_database),
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            dblimit = await crud_create_limit_by_id(db, resource_limit)
    
    if not dblimit:
        return HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"User with resource limit already created"
        )

    return ResourceLimitInResponse(resource_limit=ResourceLimitBase(**dblimit.dict()))

@router.get("/resources/limit/{user_id}",
    response_model=ResourceLimitInResponse,
    tags=["ADMIN Resources Limit"]
)
async def get_resource_limit_by_user_id(
        user_id: OID = Path(...),
        db: AsyncIOMotorClient = Depends(get_database),
):
    dblimit = await crud_get_limit_by_id(db, user_id)

    if not dblimit:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Resource limit with user id '{user_id}' not found"
        )

    return ResourceLimitInResponse(resource_limit=ResourceLimitBase(**dblimit.dict()))

@router.patch("/resources/limit/{user_id}",
    response_model=ResourceLimitInResponse,
    tags=["ADMIN Resources Limit"]
)
async def update_resource_limit_by_user_id(
        user_id: OID = Path(...),
        resource_limit: ResourceLimitInUpdate = Body(..., embed=False),
        db: AsyncIOMotorClient = Depends(get_database),
):
    dblimit = await crud_update_limit_by_id(db, user_id, resource_limit)

    if not dblimit:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Resource limit with user id '{user_id}' not found"
        )

    return ResourceLimitInResponse(resource_limit=ResourceLimitBase(**dblimit.dict()))