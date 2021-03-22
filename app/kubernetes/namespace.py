from kubernetes import client
from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client.rest import ApiException

def create_namespace(core_v1_api: CoreV1Api, name: str):
    body = client.V1Namespace(
        api_version="v1",
        kind="Namespace",
        metadata=client.V1ObjectMeta(
            name=name
        )
    )
    
    try:
        return core_v1_api.create_namespace(body=body)
    except ApiException as e:
        return e

def delete_namespace(core_v1_api: CoreV1Api, name: str):
    try:
        return core_v1_api.delete_namespace(name=name)
    except ApiException as e:
        return e