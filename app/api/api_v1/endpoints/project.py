from fastapi import APIRouter, Body, Depends, Path
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.core.jwt_v2 import get_current_user_authorizer
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.crud.project import db_create_project
from app.models.user import User
from app.models.project import ProjectBase, ProjectInResponse, ProjectInCreate

router = APIRouter()

#TODO
# @router.get("/projects/{id}", response_model=ProjectBase, tags=["projects"])
# async def get_project(
#     id: int = Path(..., ge=1),
#     user: User = Depends(get_current_user_authorizer()),
#     db: AsyncIOMotorClient = Depends(get_database)
# ):
#     await get_project_or_404(db, id, user)
#     return ProjectBase(name=)

@router.post(
    "/projects",
    response_model=ProjectInResponse,
    tags=["projects"],
    status_code=HTTP_201_CREATED,
)
async def create_project(
        project: ProjectInCreate = Body(..., embed=True),
        user: User = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database),
):
    project.created_by_id = user.id
    
    async with await db.start_session() as s:
        async with s.start_transaction():
            dbproject = await db_create_project(db, project)

    return ProjectInResponse(project=ProjectBase(**dbproject.dict()))


#TODO
# @router.put("/user", response_model=ProjectInResponse, tags=["projects"])
# async def update_current_user(
#     user: UserInUpdate = Body(..., embed=True),
#     current_user: User = Depends(get_current_user_authorizer()),
#     db: AsyncIOMotorClient = Depends(get_database),
# ):
#     if user.username == current_user.username:
#         user.username = None
#     if user.email == current_user.email:
#         user.email = None

#     await check_free_username_and_email(db, user.username, user.email)

#     dbuser = await update_user(db, current_user.username, user)
#     return ProjectInResponse(project=User(**dbuser.dict(), token=current_user.token))
