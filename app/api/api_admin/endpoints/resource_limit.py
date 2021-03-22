from fastapi import APIRouter, Body, Depends, Path, HTTPException
from kubernetes.client.api.core_v1_api import CoreV1Api

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.models.resource_quota import (
    ResourceQuotaInUpdate, 
    ResourceQuotaInResponse
)
from app.models.rwmodel import OID
import app.kubernetes.resource_quota as k8s_resource_quota
from app.kubernetes import get_k8s_core_v1_api

router = APIRouter()

@router.get("/resources/limit/{user_id}",
    response_model=ResourceQuotaInResponse,
    tags=["ADMIN Resources Limit"]
)
async def get_resource_limit_by_user_id(
    user_id: OID = Path(...),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api)
):
    quota = k8s_resource_quota.get_resource_quota(core_v1_api=core_v1_api, name=str(user_id))

    return ResourceQuotaInResponse(resource_quota=k8s_resource_quota.convert_to_ResourceQuotaBase(quota))

@router.patch("/resources/limit/{user_id}",
    response_model=ResourceQuotaInResponse,
    tags=["ADMIN Resources Limit"]
)
async def update_resource_limit_by_user_id(
        user_id: OID = Path(...),
        quota: ResourceQuotaInUpdate = Body(..., embed=False),
        core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api)
):
    hard_dict = k8s_resource_quota.convert_to_dict(quota)
    quota = k8s_resource_quota.update_resource_quota(core_v1_api=core_v1_api, name=str(user_id), hard_dict=hard_dict)

    return ResourceQuotaInResponse(resource_quota=k8s_resource_quota.convert_to_ResourceQuotaBase(quota))