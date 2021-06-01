from typing import Optional
from fastapi import APIRouter, Body, Depends, Path
from fastapi.param_functions import Query
from fastapi.responses import Response
from kubernetes.client import ApiClient, CoreV1Api, NetworkingV1beta1Api

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)

from app.core.jwt import get_current_user_authorizer
from app.core.permission import check_permission_with_exception
from app.models.route import RoleEnum
from app.models.rwmodel import OID
from app.models.pod import (
    PodInCreate,
    PodInResponse,
    PodInResponseStatus,
    ManyPodInResponse,
    PodInUpdate
)
from app.models.user import User
from app.models.k8s_resource.io.k8s.api.core.v1 import PodStatus

import app.kubernetes.pod as k8s_pod
import app.kubernetes.service as k8s_service
import app.kubernetes.ingress as k8s_ingress
from app.kubernetes import get_k8s_core_v1_api, get_k8s_networking_v1_api, get_k8s_v1_api
from app.grafana.dashboard import delete_dashboard_by_uid

router = APIRouter()

@router.get("/resources/pod/{user_id}/{name}",
    response_model=PodInResponse,
    response_model_exclude_none=True,
    tags=["ADMIN Resources"]
)
async def get_pod_by_name(
    user_id: OID = Path(...),
    name: str = Path(...),
    current_user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api),
    v1_api: ApiClient = Depends(get_k8s_v1_api)
):
    check_permission_with_exception(current_user.roles, RoleEnum.SUPER)
    namespace = str(user_id)

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


@router.get("/resources/pod/{user_id}/{name}/status",
    response_model=PodInResponseStatus,
    response_model_exclude_none=True,
    tags=["ADMIN Resources"]
)
async def get_pod_status_by_name(
    user_id: OID = Path(...),
    name: str = Path(...),
    current_user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api),
    v1_api: ApiClient = Depends(get_k8s_v1_api)
):
    check_permission_with_exception(current_user.roles, RoleEnum.SUPER)
    namespace = str(user_id)

    body = k8s_pod.get_status(core_v1_api=core_v1_api, name=name, namespace=namespace)

    return PodInResponseStatus(status=PodStatus(**v1_api.sanitize_for_serialization(body)))


@router.get("/resources/pod/{user_id}/{name}/log",
    response_model=str,
    tags=["ADMIN Resources"]
)
async def get_pod_log_by_name(
    user_id: OID = Path(...),
    name: str = Path(...),
    current_user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api)
):
    check_permission_with_exception(current_user.roles, RoleEnum.SUPER)
    namespace = str(user_id)

    body = k8s_pod.get_log(core_v1_api=core_v1_api, name=name, namespace=namespace)

    return body

@router.get("/resources/pod/{user_id}",
    response_model=ManyPodInResponse,
    tags=["ADMIN Resources"]
)
async def get_pods_name(
    user_id: OID = Path(...),
    current_user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api)
):
    check_permission_with_exception(current_user.roles, RoleEnum.SUPER)
    namespace = str(user_id)

    body = k8s_pod.get_pods(core_v1_api=core_v1_api, namespace=namespace)

    return ManyPodInResponse(pod=[item.metadata.name for item in body.items])

@router.delete(
    "/resources/pod/{user_id}/{name}",
    tags=["ADMIN Resources"],
    status_code=HTTP_204_NO_CONTENT
)
async def delete_pod(
    user_id: OID = Path(...),
    name: str = Path(...),
    current_user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api),
    networking_v1_api: NetworkingV1beta1Api = Depends(get_k8s_networking_v1_api),
):
    check_permission_with_exception(current_user.roles, RoleEnum.SUPER)
    namespace = str(user_id)

    if(k8s_ingress.check_bound(networking_v1_api=networking_v1_api, name=name, namespace=namespace)):
        k8s_ingress.delete_ingress(networking_v1_api=networking_v1_api, name=name, namespace=namespace)
        k8s_service.delete_service(core_v1_api=core_v1_api, name=name, namespace=namespace)

    k8s_pod.delete_pod(core_v1_api=core_v1_api, name=name, namespace=namespace)
    delete_dashboard_by_uid(f'{namespace}-{name}')

    return Response(status_code=HTTP_204_NO_CONTENT)
