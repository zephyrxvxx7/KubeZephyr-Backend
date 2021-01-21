from typing import Optional

from app.models.dbmodel import DBModelMixin
from app.models.rwmodel import MongoModel, OID

class ResourceUsedBase(MongoModel):
    volume_storage_used: float
    pod_used: int
    cpu_used: float
    memory_used: int

    class Config:
        schema_extra = {
            'example': [
                {
                    'volume_storage_used': 0.5, # 0.5 Gigabyte
                    'pod_used': 5, # 5 pods
                    'cpu_used': 0.5, # 0.5 cpu = 500m
                    'memory_used': 128 # 128Mi
                }
            ]
        }

class ResourceUsedInDB(DBModelMixin, ResourceUsedBase):
    user_id: OID

class ResourceUsedInCreate(ResourceUsedBase):
    user_id: OID

    class Config:
        schema_extra = {
            'example': [
                {
                    'volume_storage_used': 0,
                    'pod_used': 0,
                    'cpu_used': 0,
                    'memory_used': 0,
                    'user_id': "5ff4233f8e306b7d1ebb5b81" # Object ID
                }
            ]
        }

class ResourceUsedInUpdate(ResourceUsedBase):
    volume_storage_used: Optional[float] = None
    pod_used: Optional[int] = None
    cpu_used: Optional[float] = None
    memory_used: Optional[int] = None

class ResourceUsedInResponse(MongoModel):
    resource_used: ResourceUsedBase

