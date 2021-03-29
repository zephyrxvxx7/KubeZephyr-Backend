from fastapi import APIRouter

from .pod import router as pod_router

router = APIRouter()
router.include_router(pod_router)