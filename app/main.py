from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from kubernetes import config

from .api.api_user.api import router as api_router_user
from .api.api_admin.api import router as api_router_admin
from .core.config import ALLOWED_HOSTS, API_V1_STR, API_ADMIN_STR, PROJECT_NAME, K8S_CLIENT_IN_CLUSTER
from .core.errors import http_422_error_handler, http_error_handler
from .db.mongodb_utils import close_mongo_connection, connect_to_mongo

if K8S_CLIENT_IN_CLUSTER:
    config.load_incluster_config()
else:
    config.load_kube_config()

app = FastAPI(title=PROJECT_NAME)

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

app.include_router(api_router_user, prefix=API_V1_STR)
app.include_router(api_router_admin, prefix=API_ADMIN_STR)
