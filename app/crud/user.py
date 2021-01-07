from pydantic import EmailStr
# from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder

from app.models.rwmodel import MongoModel
from app.db.mongodb import AsyncIOMotorClient
from ..core.config import database_name, users_collection_name
from ..models.user import UserInCreate, UserInDB, UserInUpdate


async def get_user(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"username": username})
    if row:
        return UserInDB(**row)


async def get_user_by_email(conn: AsyncIOMotorClient, email: EmailStr) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"email": email})
    if row:
        return UserInDB(**row)


async def create_user(conn: AsyncIOMotorClient, user: UserInCreate) -> UserInDB:
    dbuser = UserInDB(**user.dict())
    dbuser.change_password(user.password)

    row = await conn[database_name][users_collection_name].insert_one(MongoModel.mongo(dbuser))

    dbuser.id = row.inserted_id
    dbuser.updated_at = dbuser.id.generation_time
    dbuser.created_at = dbuser.id.generation_time

    await conn[database_name][users_collection_name].update_one(
        {"_id": dbuser.id}, {"$set": MongoModel.mongo(dbuser)}
    )

    return dbuser


async def update_user(conn: AsyncIOMotorClient, username: str, user: UserInUpdate) -> UserInDB:
    dbuser = await get_user(conn, username)

    dbuser.username = user.username or dbuser.username
    dbuser.email = user.email or dbuser.email
    dbuser.bio = user.bio or dbuser.bio
    dbuser.image = user.image or dbuser.image
    if user.password:
        dbuser.change_password(user.password)

    updated_at = await conn[database_name][users_collection_name]\
        .update_one({"username": dbuser.username}, {'$set': dbuser.dict()})
    dbuser.updated_at = updated_at
    return dbuser
