from kubernetes.client import (
    ApiException,
    CoreV1Api,
    V1Namespace,
    V1ObjectMeta
)

def create_namespace(core_v1_api: CoreV1Api, name: str):
    body = V1Namespace(
        api_version="v1",
        kind="Namespace",
        metadata=V1ObjectMeta(
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