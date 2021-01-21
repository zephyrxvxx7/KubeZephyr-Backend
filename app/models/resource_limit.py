from typing import Optional

from app.models.dbmodel import DBModelMixin
from app.models.rwmodel import MongoModel, OID

class ResourceLimitBase(MongoModel):
    volume_storage_limit: float
    pod_limit: int
    cpu_limit: float
    memory_limit: int

    class Config:
        schema_extra = {
            'example': [
                {
                    'volume_storage_limit': 0.5, # 0.5 Gigabyte
                    'pod_limit': 5, # maximum 5 pods
                    'cpu_limit': 0.5, # 0.5 cpu = 500m
                    'memory_limit': 128 # 128Mi
                }
            ]
        }

class ResourceLimitInDB(DBModelMixin, ResourceLimitBase):
    user_id: OID

class ResourceLimitInCreate(ResourceLimitBase):
    user_id: OID

    class Config:
        schema_extra = {
            'example': [
                {
                    'volume_storage_limit': 0.5, # 0.5 Gigabyte
                    'pod_limit': 5, # maximum 5 pods
                    'cpu_limit': 0.5, # 0.5 cpu = 500m
                    'memory_limit': 128, # 128Mi
                    'user_id': "5ff4233f8e306b7d1ebb5b81" # Object ID
                }
            ]
        }

class ResourceLimitInUpdate(ResourceLimitBase):
    volume_storage_limit: Optional[float] = None
    pod_limit: Optional[int] = None
    cpu_limit: Optional[float] = None
    memory_limit: Optional[int] = None

class ResourceLimitInResponse(MongoModel):
    resource_limit: ResourceLimitBase

