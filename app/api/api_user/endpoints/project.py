from fastapi import APIRouter, Body, Depends, Path, HTTPException
from fastapi.responses import Response

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.core.jwt import get_current_user_authorizer
from app.crud.project import (
    crud_create_project,
    crud_get_project_by_id,
    crud_get_many_project,
    crud_update_project_by_id,
    crud_delete_project_by_id
) 
from app.db.mongodb import (
    AsyncIOMotorClient, 
    get_database
)
from app.models.rwmodel import OID
from app.models.user import User
from app.models.project import (
    ProjectInCreate,
    ProjectInResponse,
    ManyProjectInResponse,
    ProjectInUpdate
)

router = APIRouter()

@router.post(
    "/projects",
    response_model=ProjectInResponse,
    tags=["projects"],
    status_code=HTTP_201_CREATED,
)
async def create_project(
        project: ProjectInCreate = Body(..., embed=False),
        user: User = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database),
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            dbproject = await crud_create_project(db, project, user)

    return ProjectInResponse(project=dbproject)

@router.get(
    "/projects",
    response_model=ManyProjectInResponse,
    tags=["projects"]
)
async def get_project(
        user: User = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database),
):
    dbproject = await crud_get_many_project(db, user)
    
    if not dbproject:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"User did not created any Projects"
        )

    return ManyProjectInResponse(project=[pro for pro in dbproject])

@router.get(
    "/projects/{id}",
    response_model=ProjectInResponse,
    tags=["projects"]
)
async def get_project_by_id(
        id: OID = Path(...),
        user: User = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database),
):
    dbproject = await crud_get_project_by_id(db, id, user)

    if not dbproject:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Project with id '{id}' not found"
        )
    
    return ProjectInResponse(project=dbproject)

@router.put(
    "/projects/{id}",
    response_model=ProjectInResponse,
    tags=["projects"]
)
async def update_project_by_id(
        id: OID = Path(...),
        project: ProjectInUpdate = Body(..., embed=False),
        user: User = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database)
):
    dbproject = await crud_update_project_by_id(db, id, project, user)

    if not dbproject:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Project with id '{id}' not found"
        )

    return ProjectInResponse(project=dbproject)

@router.delete(
    "/projects/{id}",
    tags=["projects"],
    status_code=HTTP_204_NO_CONTENT
)
async def delete_project_by_id(
        id: OID = Path(...),
        user: User = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database)
):
    dbproject = await crud_delete_project_by_id(db, id, user)

    if not dbproject:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Project with id '{id}' not found"
        )

    return Response(status_code=HTTP_204_NO_CONTENT)