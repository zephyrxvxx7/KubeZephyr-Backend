from fastapi import HTTPException

from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client.api_client import ApiClient
from kubernetes.client.rest import ApiException
from kubernetes.client.models.v1_persistent_volume_claim import V1PersistentVolumeClaim
from kubernetes.client.models.v1_persistent_volume_claim_list import V1PersistentVolumeClaimList
from kubernetes.client.models.v1_status import V1Status

from app.models.pvc import (
    PvcInCreate, 
    PvcInUpdate
)

def create_pvc(core_v1_api: CoreV1Api, v1_api: ApiClient, namespace: str, pvc: PvcInCreate) -> V1PersistentVolumeClaim:
    body = v1_api._ApiClient__deserialize(pvc.dict(exclude_none=True), 'V1PersistentVolumeClaim')

    try:
        return core_v1_api.create_namespaced_persistent_volume_claim(namespace=namespace, body=body)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )

def get_pvc(core_v1_api: CoreV1Api, name: str, namespace: str) -> V1PersistentVolumeClaim:
    try:
        return core_v1_api.read_namespaced_persistent_volume_claim(name=name, namespace=namespace)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )

def get_pvcs(core_v1_api: CoreV1Api, namespace: str) -> V1PersistentVolumeClaimList:
    try:
        return core_v1_api.list_namespaced_persistent_volume_claim(namespace=namespace)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )

def update_pvc(core_v1_api: CoreV1Api, v1_api: ApiClient, name: str, namespace: str,  pvc: PvcInUpdate) -> V1PersistentVolumeClaim:
    body = v1_api._ApiClient__deserialize(pvc.dict(exclude_none=True), 'V1PersistentVolumeClaim')

    try:
        return core_v1_api.patch_namespaced_persistent_volume_claim(name=name, namespace=namespace, body=body)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )

def delete_pvc(core_v1_api: CoreV1Api, name: str, namespace: str) -> V1Status:

    try:
        return core_v1_api.delete_namespaced_persistent_volume_claim(name=name, namespace=namespace)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )