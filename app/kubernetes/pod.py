from fastapi import HTTPException

from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client.api_client import ApiClient
from kubernetes.client.rest import ApiException
from kubernetes.client.models.v1_pod import V1Pod
from kubernetes.client.models.v1_pod_status import V1PodStatus
from kubernetes.client.models.v1_pod_list import V1PodList
from kubernetes.client.models.v1_status import V1Status

from app.models.pod import (
    PodInCreate, 
    PodInUpdate
)

def create_pod(core_v1_api: CoreV1Api, v1_api: ApiClient, namespace: str, pod: PodInCreate) -> V1Pod:
    body = v1_api._ApiClient__deserialize(pod.dict(exclude_none=True), 'V1Pod')

    try:
        return core_v1_api.create_namespaced_pod(namespace=namespace, body=body)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )
    
def get_pod(core_v1_api: CoreV1Api, name: str, namespace: str) -> V1Pod:
    try:
        return core_v1_api.read_namespaced_pod(name=name, namespace=namespace)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )

def get_status(core_v1_api: CoreV1Api, name: str, namespace: str) -> V1PodStatus:
    try:
        return core_v1_api.read_namespaced_pod_status(name=name, namespace=namespace).status
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )

def get_log(core_v1_api: CoreV1Api, name: str, namespace: str) -> str:
    try:
        return core_v1_api.read_namespaced_pod_log(name=name, namespace=namespace)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )
    
def get_pods(core_v1_api: CoreV1Api, namespace: str) -> V1PodList:
    try:
        return core_v1_api.list_namespaced_pod(namespace=namespace)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )

def update_pod(core_v1_api: CoreV1Api, v1_api: ApiClient, name: str, namespace: str,  pod: PodInUpdate) -> V1Pod:
    body = v1_api._ApiClient__deserialize(pod.dict(exclude_none=True), 'V1Pod')

    try:
        return core_v1_api.patch_namespaced_pod(name=name, namespace=namespace, body=body)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )

def delete_pod(core_v1_api: CoreV1Api, name: str, namespace: str) -> V1Status:

    try:
        return core_v1_api.delete_namespaced_pod(name=name, namespace=namespace)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )