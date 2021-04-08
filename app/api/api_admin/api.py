from fastapi import APIRouter

from .endpoints.resource_quota import router as resource_quota_router
from .endpoints.resource_used import router as resource_used_router
from .endpoints.user import router as user_router

router = APIRouter()
router.include_router(resource_quota_router)
router.include_router(resource_used_router)
router.include_router(user_router)
