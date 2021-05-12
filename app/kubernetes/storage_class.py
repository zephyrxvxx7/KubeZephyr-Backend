from kubernetes.client import (
    ApiException,
    StorageV1Api,
    V1ObjectMeta,
    V1StorageClass,
)

from app.core.config import K8S_CEPH_NAMESPACE, K8S_CEPHBLOCKPOOL_NAME

def create_storage_class(storage_v1_api: StorageV1Api, name: str):
    body = V1StorageClass(
        api_version="storage.k8s.io/v1",
        kind="StorageClass",
        metadata=V1ObjectMeta(
            name=name
        ),
        provisioner="rook-ceph.rbd.csi.ceph.com",
        parameters={
            "clusterID": K8S_CEPH_NAMESPACE,
            "pool": K8S_CEPHBLOCKPOOL_NAME,
            "imageFormat": "2",
            "imageFeatures": "layering",
            "csi.storage.k8s.io/provisioner-secret-name": "rook-csi-rbd-provisioner",
            "csi.storage.k8s.io/provisioner-secret-namespace": K8S_CEPH_NAMESPACE,
            "csi.storage.k8s.io/controller-expand-secret-name": "rook-csi-rbd-provisioner",
            "csi.storage.k8s.io/controller-expand-secret-namespace": K8S_CEPH_NAMESPACE,
            "csi.storage.k8s.io/node-stage-secret-name": "rook-csi-rbd-node",
            "csi.storage.k8s.io/node-stage-secret-namespace": K8S_CEPH_NAMESPACE,
            "csi.storage.k8s.io/fstype": "ext4"
        },
        allow_volume_expansion=True,
        reclaim_policy="Delete"
    )

    try:
        return storage_v1_api.create_storage_class(body=body)
    except ApiException as e:
        return e

def delete_storage_class(storage_v1_api: StorageV1Api, name: str):
    try:
        return storage_v1_api.delete_storage_class(name=name)
    except ApiException as e:
        return e
