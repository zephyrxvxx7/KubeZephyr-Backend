from typing import List, Optional

from app.models.rwmodel import OID
from app.models.resource_used import (
    ResourceUsedInDB,
    ResourceUsedInCreate, 
    ResourceUsedInUpdate
)
from app.db.mongodb import AsyncIOMotorClient
from app.core.config import database_name, resources_used_collection_name
from app.core.utils import get_utcnow

async def init_resource_used(
    conn: AsyncIOMotorClient, user_id: OID
) -> ResourceUsedInDB:
    
    init_used = ResourceUsedInCreate(
        volume_storage_used = 0,
        pod_used = 0,
        cpu_used = 0,
        memory_used = 0,
        user_id = user_id
    )

    return await crud_create_used_by_id(conn, init_used)

async def crud_create_used_by_id(
    conn: AsyncIOMotorClient, used: ResourceUsedInCreate
) -> ResourceUsedInDB:
    dbused = ResourceUsedInDB(**used.dict())

    dbused.created_at = dbused.updated_at = get_utcnow()

    if await crud_get_used_by_id(conn, dbused.user_id):
        return None
    
    await conn[database_name][resources_used_collection_name].insert_one(ResourceUsedInDB.mongo(dbused))
    
    return dbused

async def crud_get_used_by_id(
    conn: AsyncIOMotorClient, user_id: OID
) -> ResourceUsedInDB:
    used_doc = await conn[database_name][resources_used_collection_name].find_one({"user_id": user_id})
    
    if used_doc:
        return ResourceUsedInDB.from_mongo(used_doc)
    
    return None

async def crud_update_used_by_id(
    conn: AsyncIOMotorClient, user_id: OID, used: ResourceUsedInUpdate
) -> ResourceUsedInDB:
    dbused = await crud_get_used_by_id(conn, user_id)

    if not dbused:
        return None

    update_data = used.dict(exclude_unset=True)
    dbused = dbused.copy(update=update_data)

    dbused.updated_at = get_utcnow()

    await conn[database_name][resources_used_collection_name].update_one(
        {"user_id": user_id}, {'$set': ResourceUsedInDB.mongo(dbused)}
    )

    return dbused

