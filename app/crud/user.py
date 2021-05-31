from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client.api.storage_v1_api import StorageV1Api
from pydantic import EmailStr
from typing import List

from app.db.mongodb import AsyncIOMotorClient
from app.core.utils import get_utcnow
from app.core.config import database_name, users_collection_name
from app.models.user import User, UserInCreate, UserInDB, UserInUpdate
from app.models.rwmodel import OID
from app.kubernetes.namespace import create_namespace
from app.kubernetes.resource_quota import create_resource_quota
from app.kubernetes.storage_class import create_storage_class
from app.grafana.alerting_notification_channel import generate_alert_channel_template, create_alert_channel

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

async def get_user_by_user_id(conn: AsyncIOMotorClient, id: OID) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"_id": id})
    if row:
        return UserInDB.from_mongo(row)
    else:
        return None

async def get_user_by_real_name(conn: AsyncIOMotorClient, realName: str) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"realName": realName})
    if row:
        return UserInDB.from_mongo(row)
    else:
        return None

async def crud_get_many_user(conn: AsyncIOMotorClient) -> List[UserInDB]:
    user_doc = conn[database_name][users_collection_name].find()
    
    if not user_doc:
        return None
    
    result = list()
    async for user in user_doc:
        result.append(UserInDB.from_mongo(user))
    
    return result


async def create_user(conn: AsyncIOMotorClient, user: UserInCreate, core_v1_api: CoreV1Api, storage_v1_api: StorageV1Api) -> UserInDB:
    dbuser = UserInDB(**user.dict())
    dbuser.change_password(user.password)
    
    dbuser.created_at = dbuser.updated_at = get_utcnow()

    await conn[database_name][users_collection_name].insert_one(UserInDB.mongo(dbuser))
    dbuser = await init_user(conn, dbuser, core_v1_api, storage_v1_api)

    return dbuser


async def init_user(conn: AsyncIOMotorClient, dbuser: UserInDB, core_v1_api: CoreV1Api, storage_v1_api: StorageV1Api):
    dbuser = await get_user_by_email(conn, dbuser.email)

    if(next((True for role in dbuser.roles if role.value == "user"), False)):
        create_namespace(core_v1_api, name=str(dbuser.id))
        create_resource_quota(core_v1_api, name=str(dbuser.id), hard_dict={
            "limits.cpu": "1",
            "limits.memory": "128Mi",
            "pods": "4",
            "persistentvolumeclaims": "4",
            "requests.storage": "5Gi"
        })
        create_storage_class(storage_v1_api, str(dbuser.id))
        create_alert_channel(generate_alert_channel_template(user=User(**dbuser.dict(), token='')))

    return dbuser


async def update_user(conn: AsyncIOMotorClient, email: EmailStr, user: UserInUpdate) -> UserInDB:
    dbuser = await get_user_by_email(conn, email)

    dbuser.email = user.email or dbuser.email
    dbuser.realName = user.realName or dbuser.realName
    dbuser.desc = user.desc or dbuser.desc
    if user.password:
        dbuser.change_password(user.password)
    
    dbuser.updated_at = get_utcnow()

    await conn[database_name][users_collection_name].update_one(
        {"_id": dbuser.id}, {'$set': dbuser.mongo()}
    )

    return dbuser

async def delete_user(conn: AsyncIOMotorClient, id: OID):
    dbuser = await get_user_by_user_id(conn, id)
    
    if not dbuser:
        return False
    
    await conn[database_name][users_collection_name].delete_one(
        {"_id": dbuser.id}
    )

    return True
