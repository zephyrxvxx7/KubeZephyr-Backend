from fastapi import APIRouter, Body, Depends, Path
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.core.jwt import get_current_user_authorizer
from app.crud.project import (
    db_create_project,
    db_get_project_by_id,
    db_get_many_project
) 
from app.db.mongodb import (
    AsyncIOMotorClient, 
    get_database
)
from app.models.rwmodel import OID
from app.models.user import UserInDB
from app.models.project import (
    ProjectBase, 
    ProjectInResponse,
    ManyProjectInResponse,
    ProjectInCreate
)

router = APIRouter()

@router.post(
    "/project",
    response_model=ProjectInResponse,
    tags=["projects"],
    status_code=HTTP_201_CREATED,
)
async def create_project(
        project: ProjectInCreate = Body(..., embed=True),
        user: UserInDB = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database),
):
    project.owner_id = user.id

    async with await db.start_session() as s:
        async with s.start_transaction():
            dbproject = await db_create_project(db, project)

    return ProjectInResponse(project=ProjectBase(**dbproject.dict()))

@router.get(
    "/project",
    response_model=ManyProjectInResponse,
    tags=["projects"]
)
async def get_project(
        user: UserInDB = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database),
):
    dbproject = await db_get_many_project(db, user)
    
    if not dbproject:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"User did not created any Projects"
        )

    return ManyProjectInResponse(project=[ProjectBase(**pro.dict()) for pro in dbproject])

@router.get(
    "/project/{id}",
    response_model=ProjectBase,
    tags=["projects"]
)
async def get_project_by_id(
        id: OID = Path(...),
        user: UserInDB = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database),
):
    dbproject = await db_get_project_by_id(db, id, user)

    if not dbproject:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Project with id '{id}' not found"
        )

    return ProjectInResponse(project=ProjectBase(**dbproject.dict()))