from typing import Optional
from fastapi import APIRouter, Body, Depends, Path, WebSocket
from fastapi.param_functions import Query
from fastapi.responses import Response
from kubernetes.client.api.core_v1_api import CoreV1Api


from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from kubernetes.client.api_client import ApiClient

from app.core.jwt import get_current_user_authorizer
import app.kubernetes.pod as k8s_pod
from app.kubernetes.pod_exec import ConnectionManager
from app.kubernetes import get_k8s_core_v1_api, get_k8s_v1_api
from app.models.pod import (
    PodInCreate,
    PodInResponse,
    PodInResponseStatus,
    ManyPodInResponse,
    PodInUpdate
)
from app.models.user import User
from app.models.k8s_resource.io.k8s.api.core.v1 import PodStatus

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
    if type(pod.metadata.labels) == dict:
        pod.metadata.labels.update({"app": pod.metadata.name})
    else:
        pod.metadata.labels = {"app": pod.metadata.name}

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

    body = k8s_pod.get_pod(core_v1_api=core_v1_api, name=name, namespace=namespace)

    # Clean up the name is default-token volume
    for index, volume in enumerate(body.spec.volumes):
        if('default-token' in volume.name):
            body.spec.volumes.pop(index)

    if(body.spec.volumes == []):
        body.spec.volumes = None
    
    for index, volume_mount in enumerate(body.spec.containers[0].volume_mounts):
        if('default-token' in volume_mount.name):
            body.spec.containers[0].volume_mounts.pop(index)
    
    if(body.spec.containers[0].volume_mounts == []):
        body.spec.containers[0].volume_mounts = None

    return PodInResponse(pod=PodInCreate(**v1_api.sanitize_for_serialization(body)))


@router.get("/resources/pod/{name}/status",
    response_model=PodInResponseStatus,
    response_model_exclude_none=True,
    tags=["Resources"]
)
async def get_pod_status_by_name(
    name: str = Path(...),
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api),
    v1_api: ApiClient = Depends(get_k8s_v1_api)
):
    namespace = str(user.id)

    body = k8s_pod.get_status(core_v1_api=core_v1_api, name=name, namespace=namespace)

    return PodInResponseStatus(status=PodStatus(**v1_api.sanitize_for_serialization(body)))


@router.get("/resources/pod/{name}/log",
    response_model=str,
    tags=["Resources"]
)
async def get_pod_log_by_name(
    name: str = Path(...),
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api)
):
    namespace = str(user.id)

    body = k8s_pod.get_log(core_v1_api=core_v1_api, name=name, namespace=namespace)

    return body

@router.websocket("/resources/pod/{namespace}/{name}/exec")
async def pod_exec_by_name(
    websocket: WebSocket,
    namespace: str = Path(...),
    name: str = Path(...),
    rows: Optional[int] = Query(20, gt=0),
    cols: Optional[int] = Query(80, gt=0),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api)
):
    pod_exec = ConnectionManager(core_v1_api=core_v1_api, name=name, namespace=namespace)
    await pod_exec.on_connect(websocket=websocket, rows=rows, cols=cols)
    

@router.get("/resources/pod",
    response_model=ManyPodInResponse,
    tags=["Resources"]
)
async def get_pods_name(
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api)
):
    namespace = str(user.id)

    body = k8s_pod.get_pods(core_v1_api=core_v1_api, namespace=namespace)

    return ManyPodInResponse(pod=[item.metadata.name for item in body.items])

@router.put("/resources/pod/{name}",
    response_model=PodInResponse,
    response_model_exclude_none=True,
    tags=["Resources"]
)
async def update_pod(
    name: str = Path(...),
    pod: PodInUpdate = Body(..., embed=False),
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api),
    v1_api: ApiClient = Depends(get_k8s_v1_api)
):
    namespace = str(user.id)

    body = k8s_pod.update_pod(core_v1_api=core_v1_api, v1_api=v1_api, name=name, namespace=namespace, pod=pod)

    return PodInResponse(pod=PodInCreate(**v1_api.sanitize_for_serialization(body)))


@router.delete(
    "/resources/pod/{name}",
    tags=["Resources"],
    status_code=HTTP_204_NO_CONTENT
)
async def delete_pod(
    name: str = Path(...),
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api)
):
    namespace = str(user.id)

    k8s_pod.delete_pod(core_v1_api=core_v1_api, name=name, namespace=namespace)

    return Response(status_code=HTTP_204_NO_CONTENT)
