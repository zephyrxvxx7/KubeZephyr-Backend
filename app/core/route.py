from typing import List
from kubernetes.client import CoreV1Api

from app.core.permission import check_permission
from app.models.route import RoleEnum, RouteItem
from app.models.user import User

from .route_user import generate_user_route
from .route_admin import generate_admin_route

common_route = RouteItem(**{
    'path': '/change-password',
    'name': 'ChangePassword',
    'component': '/sys/changePassword/index',
    'meta': {
        "title": 'sys.changePassword.title',
        "icon": 'carbon:password',
    },
})

def getMenuListByUser(user: User, core_v1_api: CoreV1Api) -> List[RouteItem]:
    menu = []
    
    if(check_permission(user.roles, RoleEnum.USER)):
        menu = generate_user_route(user=user, core_v1_api=core_v1_api)
    elif(check_permission(user.roles, RoleEnum.SUPER)):
        menu = generate_admin_route(user=user, core_v1_api=core_v1_api)
    
    menu.append(common_route)
    
    return menu
