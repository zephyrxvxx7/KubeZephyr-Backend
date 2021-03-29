from os import name
from fastapi import APIRouter, Body, Depends, Path, HTTPException
from kubernetes.client.api.core_v1_api import CoreV1Api

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from kubernetes.client.api_client import ApiClient

from app.core.jwt import get_current_user_authorizer
import app.kubernetes.pod as k8s_pod
from app.kubernetes import get_k8s_core_v1_api, get_k8s_v1_api
from app.models.pod import (
    PodInCreate,
    PodInResponse
)
from app.models.user import User

router = APIRouter()

@router.post("/resources/pod",
    response_model=PodInResponse,
    response_model_exclude_none=True,
    tags=["Resources"],
    status_code=HTTP_201_CREATED
)
async def create_pod(
        pod: PodInCreate = Body(..., embed=False),
        user: User = Depends(get_current_user_authorizer()),
        core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api),
        v1_api: ApiClient = Depends(get_k8s_v1_api)
):
    namespace = str(user.id)
    pod.metadata.namespace = namespace

    body = k8s_pod.create_pod(core_v1_api=core_v1_api, v1_api=v1_api, namespace=namespace, pod=pod)

    return PodInResponse(pod=PodInCreate(**v1_api.sanitize_for_serialization(body)))

@router.get("/resources/pod/{name}",
    response_model=PodInResponse,
    response_model_exclude_none=True,
    tags=["Resources"]
)
async def get_pod_by_name(
        name: str = Path(...),
        user: User = Depends(get_current_user_authorizer()),
        core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api),
        v1_api: ApiClient = Depends(get_k8s_v1_api)
):
    namespace = str(user.id)

    body = k8s_pod.get_pod(core_v1_api=core_v1_api, v1_api=v1_api, namespace=namespace, name=name)

    return PodInResponse(pod=PodInCreate(**v1_api.sanitize_for_serialization(body)))