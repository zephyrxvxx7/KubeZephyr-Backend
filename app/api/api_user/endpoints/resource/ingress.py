from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import Response
from kubernetes.client import ApiClient, CoreV1Api, NetworkingV1beta1Api

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)

from app.core.jwt import get_current_user_authorizer
import app.kubernetes.pod as k8s_pod
import app.kubernetes.service as k8s_service
import app.kubernetes.ingress as k8s_ingress
from app.kubernetes import get_k8s_core_v1_api, get_k8s_networking_v1_api, get_k8s_v1_api
from app.models.ingress import (
    IngressInCreate,
    IngressInResponse,
    ManyIngress,
    ManyIngressInResponse
)
from app.models.user import User
from app.models.k8s_resource.io.k8s.api.networking.v1beta1 import Ingress

router = APIRouter()

@router.post("/resources/ingress",
    response_model=IngressInResponse,
    response_model_exclude_none=True,
    tags=["Resources"],
    status_code=HTTP_201_CREATED
)
async def create_ingress(
    ingress: IngressInCreate = Body(..., embed=False),
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api),
    networking_v1_api: NetworkingV1beta1Api = Depends(get_k8s_networking_v1_api),
    v1_api: ApiClient = Depends(get_k8s_v1_api)
):
    namespace = str(user.id)

    pod = k8s_pod.get_pod(core_v1_api=core_v1_api, name=ingress.bound_pod_name, namespace=namespace)

    body = k8s_ingress.create_ingress(
        networking_v1_api=networking_v1_api,
        namespace=namespace,
        port=pod.spec.containers[0].ports[0].container_port,
        realName=user.realName.lower(),
        ingress=ingress
    )

    k8s_service.create_service(
        core_v1_api=core_v1_api, 
        name=ingress.bound_pod_name, 
        namespace=namespace, 
        port=pod.spec.containers[0].ports[0].container_port
    )

    return IngressInResponse(ingress=Ingress(**v1_api.sanitize_for_serialization(body)))


@router.get("/resources/ingress/{name}",
    response_model=IngressInResponse,
    response_model_exclude_none=True,
    tags=["Resources"]
)
async def get_ingress_by_name(
    name: str = Path(...),
    user: User = Depends(get_current_user_authorizer()),
    networking_v1_api: NetworkingV1beta1Api = Depends(get_k8s_networking_v1_api),
    v1_api: ApiClient = Depends(get_k8s_v1_api)
):
    namespace = str(user.id)

    body = k8s_ingress.get_ingress(networking_v1_api=networking_v1_api, name=name, namespace=namespace)

    return IngressInResponse(ingress=Ingress(**v1_api.sanitize_for_serialization(body)))


@router.get("/resources/ingress",
    response_model=ManyIngressInResponse,
    tags=["Resources"]
)
async def get_ingresses(
    user: User = Depends(get_current_user_authorizer()),
    networking_v1_api: NetworkingV1beta1Api = Depends(get_k8s_networking_v1_api)
):
    namespace = str(user.id)

    ingresses = k8s_ingress.get_ingresses(networking_v1_api=networking_v1_api, namespace=namespace).items

    return ManyIngressInResponse(ingress=[
        ManyIngress(
            name=ingress.metadata.name,
            sub_domain=ingress.spec.tls[0].hosts[0].split('.')[0],
            allow_cors=ingress.metadata.annotations.get('nginx.ingress.kubernetes.io/enable-cors', False) == 'true'
        )
        for ingress in ingresses
    ])


@router.delete(
    "/resources/ingress/{name}",
    tags=["Resources"],
    status_code=HTTP_204_NO_CONTENT
)
async def delete_ingress(
    name: str = Path(...),
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api),
    networking_v1_api: NetworkingV1beta1Api = Depends(get_k8s_networking_v1_api),
):
    namespace = str(user.id)

    k8s_ingress.delete_ingress(networking_v1_api=networking_v1_api, name=name, namespace=namespace)
    k8s_service.delete_service(core_v1_api=core_v1_api, name=name, namespace=namespace)

    return Response(status_code=HTTP_204_NO_CONTENT)
