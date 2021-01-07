from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime

from app.models.rwmodel import MongoModel
from app.models.project import (
    ProjectInDB,
    ProjectInCreate
)
from app.db.mongodb import AsyncIOMotorClient
from app.core.config import database_name, project_collection_name

#TODO
async def get_project_by_id(
    conn: AsyncIOMotorClient, id: int, username: Optional[str] = None
) -> ProjectInDB:
    project_doc = await conn[database_name][project_collection_name].find_one({"id": id})
    if project_doc:
        pass

#TODO
async def db_create_project(
    conn: AsyncIOMotorClient, project: ProjectInCreate
) -> ProjectInDB:
    dbproject = ProjectInDB(**project.dict())

    row = await conn[database_name][project_collection_name].insert_one(MongoModel.mongo(dbproject))

    dbproject.id = row.inserted_id
    dbproject.created_at = dbproject.id.generation_time
    dbproject.updated_at = dbproject.id.generation_time

    await conn[database_name][project_collection_name].update_one(
        {"_id": dbproject.id}, {"$set": MongoModel.mongo(dbproject)}
    )

    return dbproject