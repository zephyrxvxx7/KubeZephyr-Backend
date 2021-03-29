from app.models.k8s_resource.io.k8s.api.core.v1 import Namespace
from fastapi import HTTPException

from kubernetes import client
from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client.api_client import ApiClient
from kubernetes.client.rest import ApiException

from app.models.pod import (
    PodInCreate
)

def create_pod(core_v1_api: CoreV1Api, v1_api: ApiClient, namespace: str, pod: PodInCreate):
    body = v1_api._ApiClient__deserialize(pod.dict(exclude_none=True), 'V1Pod')

    try:
        return core_v1_api.create_namespaced_pod(namespace=namespace, body=body)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )
    
def get_pod(core_v1_api: CoreV1Api, v1_api: ApiClient, namespace: str, name: str):
    try:
        return core_v1_api.read_namespaced_pod(name=name, namespace=namespace)
    except ApiException as e:
        print(eval(e.body)['message'])
    
    