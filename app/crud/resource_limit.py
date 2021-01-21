from typing import List, Optional

from app.models.rwmodel import MongoModel, OID
from app.models.resource_limit import (
    ResourceLimitInDB,
    ResourceLimitInCreate, 
    ResourceLimitInUpdate
)
from app.models.user import UserInDB
from app.db.mongodb import AsyncIOMotorClient
from app.core.config import database_name, resources_limit_collection_name
from app.core.utils import get_utcnow

async def init_resource_limit(
    conn: AsyncIOMotorClient, user_id: OID
) -> ResourceLimitInDB:
    
    init_limit = ResourceLimitInCreate(
        volume_storage_limit = 5.0,
        pod_limit = 5,
        cpu_limit = 0.5,
        memory_limit = 128,
        user_id = user_id
    )

    return await crud_create_limit_by_id(conn, init_limit)

async def crud_create_limit_by_id(
    conn: AsyncIOMotorClient, limit: ResourceLimitInCreate
) -> ResourceLimitInDB:
    dblimit = ResourceLimitInDB(**limit.dict())

    dblimit.created_at = dblimit.updated_at = get_utcnow()

    if await crud_get_limit_by_id(conn, dblimit.user_id):
        return None
    
    await conn[database_name][resources_limit_collection_name].insert_one(ResourceLimitInDB.mongo(dblimit))
    
    return dblimit

async def crud_get_limit_by_id(
    conn: AsyncIOMotorClient, user_id: OID
) -> ResourceLimitInDB:
    limit_doc = await conn[database_name][resources_limit_collection_name].find_one({"user_id": user_id})
    
    if limit_doc:
        return ResourceLimitInDB.from_mongo(limit_doc)
    
    return None

async def crud_update_limit_by_id(
    conn: AsyncIOMotorClient, user_id: OID, limit: ResourceLimitInUpdate
) -> ResourceLimitInDB:
    dblimit = await crud_get_limit_by_id(conn, user_id)

    if not dblimit:
        return None

    update_data = limit.dict(exclude_unset=True)
    dblimit = dblimit.copy(update=update_data)

    dblimit.updated_at = get_utcnow()

    await conn[database_name][resources_limit_collection_name].update_one(
        {"user_id": user_id}, {'$set': ResourceLimitInDB.mongo(dblimit)}
    )

    return dblimit

