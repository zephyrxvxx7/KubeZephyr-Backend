from fastapi import HTTPException

from kubernetes.client import (
    ApiException,
    NetworkingV1beta1Api,
    NetworkingV1beta1Ingress,
    NetworkingV1beta1IngressList,
    NetworkingV1beta1IngressSpec,
    NetworkingV1beta1IngressTLS,
    NetworkingV1beta1IngressRule,
    NetworkingV1beta1HTTPIngressRuleValue,
    NetworkingV1beta1HTTPIngressPath,
    NetworkingV1beta1IngressBackend,
    V1Status,
    V1ObjectMeta,
)

from app.core.config import K8S_DOMAIN, K8S_CLUSTER_ISSUER
from app.models.ingress import (
    IngressInCreate
)

def create_ingress(networking_v1_api: NetworkingV1beta1Api, namespace: str, port: int, realName: str, ingress: IngressInCreate):
    body = NetworkingV1beta1Ingress(
        metadata=V1ObjectMeta(
            name=ingress.bound_pod_name,
            annotations={
                'kubernetes.io/ingress.class': 'nginx',
                'cert-manager.io/cluster-issuer': K8S_CLUSTER_ISSUER,
                'ingress.kubernetes.io/ssl-redirect': 'true'
            }
        ),
        spec=NetworkingV1beta1IngressSpec(
            tls=[NetworkingV1beta1IngressTLS(
                hosts=[f'{ingress.sub_domain}.{realName}.{K8S_DOMAIN}'],
                secret_name=f'{ingress.sub_domain}-{realName}-tls'
            )],
            rules=[NetworkingV1beta1IngressRule(
                host=f'{ingress.sub_domain}.{realName}.{K8S_DOMAIN}',
                http=NetworkingV1beta1HTTPIngressRuleValue(
                    paths=[NetworkingV1beta1HTTPIngressPath(
                        path="/",
                        backend=NetworkingV1beta1IngressBackend(
                            service_name=ingress.bound_pod_name,
                            service_port=port
                        )
                    )]
                )
            )]
        )
    )
    if ingress.allow_cors:
        body.metadata.annotations.update({
            'nginx.ingress.kubernetes.io/enable-cors': 'true',
            'nginx.ingress.kubernetes.io/cors-allow-origin': '*'
        })

    try:
        return networking_v1_api.create_namespaced_ingress(namespace=namespace, body=body)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )

def check_bound(networking_v1_api: NetworkingV1beta1Api, name: str, namespace: str) -> bool:
    try:
        networking_v1_api.read_namespaced_ingress(name=name, namespace=namespace)
        return True
    except ApiException:
        return False


def get_ingress(networking_v1_api: NetworkingV1beta1Api, name: str, namespace: str) -> NetworkingV1beta1Ingress:
    try:
        return networking_v1_api.read_namespaced_ingress(name=name, namespace=namespace)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )

def get_ingresses(networking_v1_api: NetworkingV1beta1Api, namespace: str) -> NetworkingV1beta1IngressList:
    try:
        return networking_v1_api.list_namespaced_ingress(namespace=namespace)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )

def delete_ingress(networking_v1_api: NetworkingV1beta1Api, name: str, namespace: str) -> V1Status:
    try:
        return networking_v1_api.delete_namespaced_ingress(name=name, namespace=namespace)
    except ApiException as e:
        raise HTTPException(
            status_code=e.status,
            detail=eval(e.body)['message']
        )