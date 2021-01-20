from pydantic import EmailStr

from datetime import datetime

from app.db.mongodb import AsyncIOMotorClient
from app.crud.resource_limit import init_resource_limit
from app.core.utils import get_utcnow
from app.core.config import database_name, users_collection_name
from ..models.user import UserInCreate, UserInDB, UserInUpdate


async def get_user(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"username": username})
    if row:
        return UserInDB.from_mongo(row)
    else:
        return None


async def get_user_by_email(conn: AsyncIOMotorClient, email: EmailStr) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"email": email})
    if row:
        return UserInDB.from_mongo(row)
    else:
        return None


async def create_user(conn: AsyncIOMotorClient, user: UserInCreate) -> UserInDB:
    dbuser = UserInDB(**user.dict())
    dbuser.change_password(user.password)
    
    dbuser.created_at = dbuser.updated_at = get_utcnow()

    await conn[database_name][users_collection_name].insert_one(UserInDB.mongo(dbuser))
    await init_user(conn, dbuser)

    return dbuser

async def init_user(conn: AsyncIOMotorClient, dbuser: UserInDB):
    dbuser = await get_user_by_email(conn, dbuser.email)

    await init_resource_limit(conn, dbuser.id)

    return True


async def update_user(conn: AsyncIOMotorClient, email: EmailStr, user: UserInUpdate) -> UserInDB:
    dbuser = await get_user_by_email(conn, email)

    dbuser.username = user.username or dbuser.username
    dbuser.email = user.email or dbuser.email
    dbuser.bio = user.bio or dbuser.bio
    dbuser.image = user.image or dbuser.image
    if user.password:
        dbuser.change_password(user.password)
    
    dbuser.updated_at = get_utcnow()

    await conn[database_name][users_collection_name].update_one(
        {"_id": dbuser.id}, {'$set': UserInDB.mongo(dbuser)}
    )

    return dbuser
