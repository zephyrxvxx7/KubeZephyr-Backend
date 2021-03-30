from fastapi import APIRouter, Body, Depends, Path
from kubernetes.client.api.core_v1_api import CoreV1Api

from starlette.status import (
    HTTP_201_CREATED
)
from kubernetes.client.api_client import ApiClient

from app.core.jwt import get_current_user_authorizer
import app.kubernetes.pvc as k8s_pvc
from app.kubernetes import get_k8s_core_v1_api, get_k8s_v1_api
from app.models.pvc import (
    PvcInCreate,
    PvcInResponse,
    ManyPvcInResponse,
    PvcInUpdate
)
from app.models.user import User

router = APIRouter()

@router.post("/resources/pvc",
    response_model=PvcInResponse,
    response_model_exclude_none=True,
    tags=["Resources"],
    status_code=HTTP_201_CREATED
)
async def create_pvc(
    pvc: PvcInCreate = Body(..., embed=False),
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api),
    v1_api: ApiClient = Depends(get_k8s_v1_api)
):
    namespace = str(user.id)
    pvc.metadata.namespace = namespace

    body = k8s_pvc.create_pvc(core_v1_api=core_v1_api, v1_api=v1_api, namespace=namespace, pvc=pvc)

    return PvcInResponse(pvc=PvcInCreate(**v1_api.sanitize_for_serialization(body)))

@router.get("/resources/pvc/{name}",
    response_model=PvcInResponse,
    response_model_exclude_none=True,
    tags=["Resources"]
)
async def get_pvc_by_name(
    name: str = Path(...),
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api),
    v1_api: ApiClient = Depends(get_k8s_v1_api)
):
    namespace = str(user.id)

    body = k8s_pvc.get_pvc(core_v1_api=core_v1_api, name=name, namespace=namespace)

    return PvcInResponse(pvc=PvcInCreate(**v1_api.sanitize_for_serialization(body)))

@router.get("/resources/pvc",
    response_model=ManyPvcInResponse,
    tags=["Resources"]
)
async def get_pvcs_name(
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api)
):
    namespace = str(user.id)

    body = k8s_pvc.get_pvcs(core_v1_api=core_v1_api, namespace=namespace)

    return ManyPvcInResponse(pvc=[item.metadata.name for item in body.items])

@router.patch("/resources/pvc/{name}",
    response_model=PvcInResponse,
    response_model_exclude_none=True,
    tags=["Resources"]
)
async def update_pvc(
    name: str = Path(...),
    pvc: PvcInUpdate = Body(..., embed=False),
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api),
    v1_api: ApiClient = Depends(get_k8s_v1_api)
):
    namespace = str(user.id)

    body = k8s_pvc.update_pvc(core_v1_api=core_v1_api, v1_api=v1_api, name=name, namespace=namespace, pvc=pvc)

    return PvcInResponse(pvc=PvcInCreate(**v1_api.sanitize_for_serialization(body)))

@router.delete("/resources/pvc/{name}",
    tags=["Resources"]
)
async def delete_pvc(
    name: str = Path(...),
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api)
):
    namespace = str(user.id)

    k8s_pvc.delete_pvc(core_v1_api=core_v1_api, name=name, namespace=namespace)

    return None