from typing import List, Optional

from slugify import slugify

from app.models.rwmodel import OID
from app.models.project import (
    ProjectInDB,
    ProjectInCreate, 
    ProjectInUpdate
)
from app.models.user import UserInDB
from app.db.mongodb import AsyncIOMotorClient
from app.core.utils import get_utcnow
from app.core.config import database_name, projects_collection_name

async def crud_create_project(
    conn: AsyncIOMotorClient, project: ProjectInCreate
) -> ProjectInDB:
    dbproject = ProjectInDB(**project.dict())

    dbproject.created_at = dbproject.updated_at = get_utcnow()
    
    await conn[database_name][projects_collection_name].insert_one(ProjectInDB.mongo(dbproject))

    return dbproject

async def crud_get_project_by_id(
    conn: AsyncIOMotorClient, id: OID, user: UserInDB
) -> ProjectInDB:
    project_doc = await conn[database_name][projects_collection_name].find_one({"_id": id})
    
    if project_doc:
        project_doc = ProjectInDB.from_mongo(project_doc)
        if project_doc.owner_id == user.id:
            return project_doc
    
    return None

async def crud_get_many_project(
    conn: AsyncIOMotorClient, user: UserInDB
) -> ProjectInDB:
    project_doc = conn[database_name][projects_collection_name].find({"owner_id": user.id})
    
    if not project_doc:
        return None
    
    result = list()
    async for project in project_doc:
        result.append(ProjectInDB.from_mongo(project))
    return result
    
    

async def crud_update_project_by_id(
    conn: AsyncIOMotorClient, id: OID, project: ProjectInUpdate, user: UserInDB
) -> ProjectInDB:

    dbproject = await crud_get_project_by_id(conn, id, user)

    if not dbproject:
        return None

    dbproject.name = project.name or dbproject.name
    dbproject.pod = project.pod or dbproject.pod
    dbproject.service = project.service or dbproject.service
    dbproject.volume = project.volume or dbproject.volume

    dbproject.updated_at = get_utcnow()

    await conn[database_name][projects_collection_name].update_one(
        {"_id": dbproject.id}, {'$set': ProjectInDB.mongo(dbproject)}
    )

    return dbproject

async def crud_delete_project_by_id(
    conn: AsyncIOMotorClient, id: OID, user: UserInDB
):
    dbproject = await crud_get_project_by_id(conn, id, user)

    if not dbproject:
        return None

    await conn[database_name][projects_collection_name].delete_one({"_id": dbproject.id})

    return True