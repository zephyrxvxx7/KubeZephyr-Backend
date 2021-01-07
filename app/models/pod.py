from os import name
from typing import Optional, List
from pydantic import BaseModel
from pydantic.types import Json

from app.models.dbmodel import DBModelMixin
from app.models.rwmodel import MongoModel

class Resource(BaseModel):
    memory: str
    cpu:  str

class PodVolume(BaseModel):
    name: str
    claimName: str

class VolumeMount(BaseModel):
    name: str
    mountPath: str

class Container(BaseModel):
    name: str
    image: str
    containerPort: int
    volumeMounts: Optional[List[VolumeMount]] = None
    resource: Optional[Resource] = None

class Pod(DBModelMixin, MongoModel):
    name: str
    containers: Container
    # volumes: Optional[List[PodVolume]] = None
    
    