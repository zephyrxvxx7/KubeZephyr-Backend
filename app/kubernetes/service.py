from fastapi import HTTPException

from kubernetes.client import (
    ApiException,
    CoreV1Api,
    V1Service,
    V1ServiceSpec,
    V1ServicePort,
    V1Status,
    V1ObjectMeta,
)


def create_service(core_v1_api: CoreV1Api, name: str, namespace: str, port: int) -> V1Service:
    body = V1Service(
        metadata=V1ObjectMeta(
            name=name
        ),
        spec=V1ServiceSpec(
            selector={
                "app": name
            },
            ports=[V1ServicePort(
                port=port,
                target_port=port
            )]
        )
    )

    try:
        return core_v1_api.create_namespaced_service(namespace=namespace, body=body)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )

def get_service(core_v1_api: CoreV1Api, name: str, namespace: str) -> V1Service:
    try:
        return core_v1_api.read_namespaced_service(name=name, namespace=namespace)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )

def delete_service(core_v1_api: CoreV1Api, name: str, namespace: str) -> V1Status: 
    try:
        return core_v1_api.delete_namespaced_service(name=name, namespace=namespace)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )
