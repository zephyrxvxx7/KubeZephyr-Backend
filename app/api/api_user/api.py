from fastapi import APIRouter

from .endpoints.authenticaion import router as auth_router
from .endpoints.user import router as user_router
from .endpoints.project import router as project_router
from .endpoints.alert_channel import router as alert_channel_router
from .endpoints.resource_quota import router as resource_quota_router
from .endpoints.resource_used import router as resource_used_router
from .endpoints.docker_hub import router as docker_hub_router
from .endpoints.resource.api import router as rosource_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(project_router)
router.include_router(alert_channel_router)
router.include_router(resource_quota_router)
router.include_router(resource_used_router)
router.include_router(docker_hub_router)
router.include_router(rosource_router)
