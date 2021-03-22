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
from app.models.resource_used import (
    ResourceUsedBase,
    ResourceUsedInUpdate,
    ResourceUsedInResponse
)
from app.models.rwmodel import OID

router = APIRouter()

@router.get("/resources/used/{user_id}",
    response_model=ResourceUsedInResponse,
    tags=["ADMIN Resources Used"]
)
async def get_resource_used_by_user_id(
        user_id: OID = Path(...),
        db: AsyncIOMotorClient = Depends(get_database),
):
    # dbused = await crud_get_used_by_id(db, user_id)
    dbused = None

    if not dbused:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Resource used with user id '{user_id}' not found"
        )

    return ResourceUsedInResponse(resource_used=ResourceUsedBase(**dbused.dict()))

@router.patch("/resources/used/{user_id}",
    response_model=ResourceUsedInResponse,
    tags=["ADMIN Resources Used"]
)
async def update_resource_used_by_user_id(
        user_id: OID = Path(...),
        resource_used: ResourceUsedInUpdate = Body(..., embed=False),
        db: AsyncIOMotorClient = Depends(get_database),
):
    # dbused = await crud_update_used_by_id(db, user_id, resource_used)
    dbused = None

    if not dbused:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Resource used with user id '{user_id}' not found"
        )

    return ResourceUsedInResponse(resource_used=ResourceUsedBase(**dbused.dict()))