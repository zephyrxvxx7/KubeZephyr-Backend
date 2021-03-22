from kubernetes import client
from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client.api.storage_v1_api import StorageV1Api

def get_k8s_core_v1_api() -> CoreV1Api:
    return client.CoreV1Api()

def get_k8s_storage_v1_api() -> StorageV1Api:
    return client.StorageV1Api()