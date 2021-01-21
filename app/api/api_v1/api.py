from fastapi import APIRouter

from .endpoints.authenticaion import router as auth_router
from .endpoints.user import router as user_router
from .endpoints.project import router as project_router
from .endpoints.resource_limit import router as resource_limit_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(project_router)
router.include_router(resource_limit_router)
