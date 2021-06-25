from typing import List
from kubernetes.client import CoreV1Api

from app.core.permission import check_permission
from app.models.route import RoleEnum, RouteItem
from app.models.user import User

from .route_user import generate_user_route
from .route_admin import generate_admin_route

def getMenuListByUser(user: User, core_v1_api: CoreV1Api) -> List[RouteItem]:
    menu = []
    
    if(check_permission(user.roles, RoleEnum.USER)):
        return generate_user_route(user=user, core_v1_api=core_v1_api)
    elif(check_permission(user.roles, RoleEnum.SUPER)):
        return generate_admin_route(user=user, core_v1_api=core_v1_api)
    
    return menu
