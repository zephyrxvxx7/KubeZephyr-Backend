from os import name
from typing import Optional
from pydantic import BaseModel

from app.models.dbmodel import DBModelMixin
from app.models.rwmodel import MongoModel

class VolumeBase(MongoModel):
    name: str
    requestsStorage: int

class Volume(DBModelMixin, MongoModel):
    pass
