from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
)

from kubernetes import client
from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client.rest import ApiException
from kubernetes.utils import parse_quantity

from app.models.resource_quota import (
    ResourceQuotaBase,
    ResourceQuotaInUpdate
)


def create_resource_quota(core_v1_api: CoreV1Api, name:str, hard_dict: dict):
    body = client.V1ResourceQuota(
        api_version="v1",
        kind="ResourceQuota",
        metadata=client.V1ObjectMeta(
            name=name
        ),
        spec=client.V1ResourceQuotaSpec(
            hard=hard_dict
        )
    )

    try:
        return core_v1_api.create_namespaced_resource_quota(namespace=name, body=body)
    except ApiException as e:
        return e

def get_resource_quota(core_v1_api: CoreV1Api, name: str):
    try:
        return core_v1_api.read_namespaced_resource_quota_status(name=name, namespace=name).status.hard
    except ApiException as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Resource quota with user not found"
        )

def get_resource_used(core_v1_api: CoreV1Api, name: str):
    try:
        return core_v1_api.read_namespaced_resource_quota_status(name=name, namespace=name).status.used
    except ApiException as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Resource used with user not found"
        )

def update_resource_quota(core_v1_api: CoreV1Api, name: str, hard_dict: dict):
    body = client.V1ResourceQuota(
        api_version="v1",
        kind="ResourceQuota",
        spec=client.V1ResourceQuotaSpec(
            hard=hard_dict
        )
    )
    try:
        return core_v1_api.patch_namespaced_resource_quota(name=name, namespace=name, body=body).spec.hard
    except ApiException as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Resource used with user not found"
        )

def convert_to_ResourceQuotaBase(_dict: dict) -> ResourceQuotaBase:
    return ResourceQuotaBase(
        limit_cpu = str(_dict['limits.cpu']),
        limit_memory = str(_dict['limits.memory']),
        persistentvolumeclaims = int(_dict['persistentvolumeclaims']),
        pods = int(_dict['pods']),
        request_storage = str(_dict['requests.storage'])
    )

def convert_to_dict(quota: ResourceQuotaInUpdate) -> dict:
    quota = quota.dict()
    
    result = {
        "limits.cpu": quota['limit_cpu'],
        "limits.memory": quota['limit_memory'],
        "persistentvolumeclaims": quota['persistentvolumeclaims'],
        "pods": quota['pods'],
        "requests.storage": quota['request_storage']
    }

    return { key: str(value) for key, value in result.items() if value is not None }