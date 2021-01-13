from typing import List, Optional

from slugify import slugify
from datetime import datetime

from app.models.rwmodel import MongoModel, OID
from app.models.project import (
    ProjectInDB,
    ProjectInCreate
)
from app.models.user import UserInDB
from app.db.mongodb import AsyncIOMotorClient
from app.core.config import database_name, project_collection_name


async def db_get_project_by_id(
    conn: AsyncIOMotorClient, id: OID, user: UserInDB
) -> ProjectInDB:
    project_doc = await conn[database_name][project_collection_name].find_one({"_id": id})
    
    if project_doc:
        project_doc = ProjectInDB.from_mongo(project_doc)
        if project_doc.owner_id == user.id:
            return project_doc
    
    return None

async def db_get_many_project(
    conn: AsyncIOMotorClient, user: UserInDB
) -> ProjectInDB:
    project_doc = conn[database_name][project_collection_name].find({"owner_id": user.id})
    
    if project_doc:
        result = list()
        async for project in project_doc:
            result.append(ProjectInDB.from_mongo(project))
        return result
    
    return None

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