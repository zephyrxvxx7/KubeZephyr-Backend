from fastapi import APIRouter

from .pod import router as pod_router
from .pvc import router as pvc_router
from .ingress import router as ingress_router

router = APIRouter()
router.include_router(pod_router)
router.include_router(pvc_router)
router.include_router(ingress_router)