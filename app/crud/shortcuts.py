from typing import Optional

from pydantic import EmailStr
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.models.project import ProjectInDB
from app.crud.user import get_user, get_user_by_email
from app.crud.project import get_project_by_id
from app.db.mongodb import AsyncIOMotorClient


async def check_free_username_and_email(
        conn: AsyncIOMotorClient, username: Optional[str] = None, email: Optional[EmailStr] = None
):
    if username:
        user_by_username = await get_user(conn, username)
        if user_by_username:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this username already exists",
            )
    if email:
        user_by_email = await get_user_by_email(conn, email)
        if user_by_email:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this email already exists",
            )

#TODO
async def get_project_or_404(
        conn: AsyncIOMotorClient, id: int, username: Optional[str] = None
) -> ProjectInDB:
    searched_project = await get_project_by_id(conn, id, username)
    if not searched_project:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Project '{id}' not found",
        )
    return searched_project