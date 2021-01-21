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
    ResourceUsedInResponse,
)
from app.crud.resource_used import (
    crud_get_used_by_id,
) 
from app.models.user import User
from app.models.rwmodel import OID

router = APIRouter()

@router.get("/resources/used",
    response_model=ResourceUsedInResponse,
    tags=["Resources Used"]
)
async def get_resource_used(
        user: User = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database),
):
    dbused = await crud_get_used_by_id(db, user.id)

    if not dbused:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Resource used with user id '{user.id}' not found"
        )

    return ResourceUsedInResponse(resource_used=ResourceUsedBase(**dbused.dict()))
