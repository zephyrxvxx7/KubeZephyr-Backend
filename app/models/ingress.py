from os import name
from typing import Dict, Optional, List
from pydantic import BaseModel, Field

from app.models.k8s_resource.io.k8s.api.networking.v1beta1 import Ingress

class IngressInCreate(BaseModel):
    bound_pod_name: str
    sub_domain: str
    allow_cors: Optional[bool] = False

class IngressInUpdate(BaseModel):
    sub_domain: Optional[str] = None

class IngressInResponse(BaseModel):
    ingress: Ingress

class ManyIngress(BaseModel):
    name: str
    sub_domain: str
    allow_cors: bool

class ManyIngressInResponse(BaseModel):
    ingress: List[ManyIngress]
