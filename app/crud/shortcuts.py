from typing import Optional

from pydantic import EmailStr
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.crud.user import get_user_by_email, get_user_by_real_name
from app.db.mongodb import AsyncIOMotorClient


async def check_free_email(
        conn: AsyncIOMotorClient, email: EmailStr
):
    user_by_email = await get_user_by_email(conn, email)
    if user_by_email:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User with the email already exists",
        )

async def check_free_real_name(
        conn: AsyncIOMotorClient, realNmae: str
):
    user_by_real_name = await get_user_by_real_name(conn, realNmae)
    if user_by_real_name:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User with the real name already exists",
        )
