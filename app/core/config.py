import os

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret
from databases import DatabaseURL

API_V1_STR = "/api"
API_ADMIN_STR = "/api/admin"

JWT_TOKEN_PREFIX = "Token"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week

KUBERNETES_KIND = ["Pod", "Service", "PersistentVolumeClaim", "Ingress"]

load_dotenv(".env")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
SECRET_KEY = Secret(os.getenv("SECRET_KEY", "secret key for project"))

PROJECT_NAME = os.getenv("PROJECT_NAME", "FastAPI example application")
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

MONGODB_URL = os.getenv("MONGODB_URL", "")  # deploying without docker-compose
MONGO_DB = os.getenv("MONGO_DB", "KubeZephyr")
if not MONGODB_URL:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 12345))
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "ji32k7au4a83")
    

    MONGODB_URL = DatabaseURL(
        f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    )
else:
    MONGODB_URL = DatabaseURL(MONGODB_URL)

K8S_CLIENT_IN_CLUSTER = os.getenv("K8S_CLIENT_IN_CLUSTER", False)
K8S_CEPH_NAMESPACE = os.getenv("K8S_CEPH_NAMESPACE", "rook-ceph")
K8S_CEPHBLOCKPOOL_NAME = os.getenv("K8S_CEPHBLOCKPOOL_NAME", "kubezephyr-blockpool")

database_name = MONGO_DB
article_collection_name = "articles"
favorites_collection_name = "favorites"
tags_collection_name = "tags"
users_collection_name = "users"
comments_collection_name = "commentaries"
followers_collection_name = "followers"
projects_collection_name = "projects"
resources_collection_name = "resources"
resources_limit_collection_name = "limit"
resources_used_collection_name = "used"