from kubernetes.client import CoreV1Api, StorageV1Api, ApiClient

def get_k8s_core_v1_api() -> CoreV1Api:
    return CoreV1Api()

def get_k8s_storage_v1_api() -> StorageV1Api:
    return StorageV1Api()

def get_k8s_v1_api() -> ApiClient:
    return ApiClient()