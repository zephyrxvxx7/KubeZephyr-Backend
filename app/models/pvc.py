from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.k8s_resource.io.k8s.api.core.v1 import PersistentVolumeClaimSpec
from app.models.k8s_resource.io.k8s.apimachinery.pkg.apis.meta.v1 import ObjectMeta
class PvcInCreate(BaseModel):
    metadata: ObjectMeta = Field(
        ...,
        description="Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata",
    )
    spec: PersistentVolumeClaimSpec = Field(
        ...,
        description='Spec defines the desired characteristics of a volume requested by a pod author. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims',
    )

class PvcInUpdate(BaseModel):
    spec: Optional[PersistentVolumeClaimSpec] = Field(
        None,
        description='Spec defines the desired characteristics of a volume requested by a pod author. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims',
    )

class PvcInResponse(BaseModel):
    pvc: PvcInCreate

class ManyPvc(BaseModel):
    name: str
    accessMode: str
    storage: str

class ManyPvcInResponse(BaseModel):
    pvc: List[ManyPvc]