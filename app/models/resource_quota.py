from typing import Optional
from pydantic import BaseModel

class ResourceQuotaBase(BaseModel):
    limit_cpu: str
    limit_memory: str
    persistentvolumeclaims: int
    pods: int
    request_storage: str

    class Config:
        schema_extra = {
            'example': [
                {   
                    'limit_cpu': '500m', # 0.5 core of CPU
                    'limit_memory': '128Mi', # 134217728 Bytes = 128Mi
                    'persistentvolumeclaims': 5, # count of PersistentVolumeClaims
                    'pods': 5, # count of pods
                    'request_storage': '5Gi', # 5368709120 = 5 Gi
                }
            ]
        }

class ResourceQuotaInUpdate(BaseModel):
    limit_cpu: Optional[str] = None
    limit_memory: Optional[str] = None
    persistentvolumeclaims: Optional[int] = None
    pods: Optional[int] = None
    request_storage: Optional[str] = None

    class Config:
        schema_extra = {
            'example': [
                {   
                    'limit_cpu': 0.5, # 0.5 core of CPU
                    'limit_memory': 134217728, # 134217728 Bytes = 128Mi
                    'persistentvolumeclaims': 5, # count of PersistentVolumeClaims
                    'pods': 5, # count of pods
                    'request_storage': 5368709120, # 5368709120 = 5 Gi
                }
            ]
        }

class ResourceQuotaInResponse(BaseModel):
    resource_quota: ResourceQuotaBase

class ResourceUsedInResponse(BaseModel):
    resource_used: ResourceQuotaBase


