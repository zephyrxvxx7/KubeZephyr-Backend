from typing import Optional, List

from pydantic import BaseModel
from app.models.dbmodel import DBModelMixin
from app.models.rwmodel import MongoModel

class Container(BaseModel):
    name: str
    image: str
    port: int

class Service(MongoModel):
    name: str
    ports: List[str]
    containers: Container