from fastapi import APIRouter

from .endpoints.authenticaion import router as auth_router
from .endpoints.user import router as user_router
from .endpoints.project import router as project_router
from .endpoints.resource_quota import router as resource_quota_router
from .endpoints.resource_used import router as resource_used_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(project_router)
router.include_router(resource_quota_router)
router.include_router(resource_used_router)
