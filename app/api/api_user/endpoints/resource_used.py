from fastapi import APIRouter, Body, Depends, Path, HTTPException
from kubernetes.client.api.core_v1_api import CoreV1Api

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.core.jwt import get_current_user_authorizer
import app.kubernetes.resource_quota as k8s_resource_quota
from app.kubernetes import get_k8s_core_v1_api
from app.models.resource_quota import ResourceUsedInResponse
from app.models.user import User

router = APIRouter()

@router.get("/resources/used",
    response_model=ResourceUsedInResponse,
    tags=["Resources"]
)
def get_resource_used(
    user: User = Depends(get_current_user_authorizer()),
    core_v1_api: CoreV1Api = Depends(get_k8s_core_v1_api)
):
    used = k8s_resource_quota.get_resource_used(core_v1_api=core_v1_api, name=str(user.id))
    
    resource_used = k8s_resource_quota.convert_to_ResourceQuotaBase(used)

    return ResourceUsedInResponse(resource_used=resource_used)
