from typing import Optional

from pydantic import EmailStr
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.models.rwmodel import OID
from app.models.project import ProjectInDB
from app.crud.user import get_user, get_user_by_email
from app.crud.project import db_get_project_by_id
from app.db.mongodb import AsyncIOMotorClient


async def check_free_email(
        conn: AsyncIOMotorClient, email: Optional[EmailStr] = None
):
    if email:
        user_by_email = await get_user_by_email(conn, email)
        if user_by_email:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this email already exists",
            )
