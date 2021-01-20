from fastapi import APIRouter

from .endpoints.resource_limit import router as resource_limit_router

router = APIRouter()
router.include_router(resource_limit_router)