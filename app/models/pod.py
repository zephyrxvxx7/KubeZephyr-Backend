from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.dbmodel import DBModelMixin
from app.models.rwmodel import MongoModel
from app.models.k8s_resource.io.k8s.api.core.v1 import PodSpec
from app.models.k8s_resource.io.k8s.apimachinery.pkg.apis.meta.v1 import ObjectMeta
class PodInCreate(BaseModel):
    metadata: ObjectMeta = Field(
        ...,
        description="Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata",
    )
    spec: PodSpec = Field(
        ...,
        description='Specification of the desired behavior of the pod. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status',
    )

class PodInUpdate(BaseModel):
    spec: Optional[PodSpec] = Field(
        None,
        description='Specification of the desired behavior of the pod. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status',
    )

class PodInResponse(BaseModel):
    pod: PodInCreate

class ManyPodInResponse(BaseModel):
    pod: List[str]