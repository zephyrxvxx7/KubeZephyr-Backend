from typing import Optional, List

from app.models.dbmodel import DBModelMixin
from app.models.rwmodel import MongoModel, OID
from app.models.pod import Pod
from app.models.service import Service

class ProjectBase(MongoModel):
    name: str
    pod: Optional[List[str]] = None
    service: Optional[List[str]] = None
    volume: Optional[List[str]] = None

class ProjectInDB(DBModelMixin, ProjectBase):
    created_by_id: OID

class ProjectInCreate(ProjectBase):
    created_by_id: Optional[OID] = None

class ProjectInResponse(MongoModel):
    project: ProjectBase