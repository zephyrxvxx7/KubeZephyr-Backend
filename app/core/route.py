from typing import List
from kubernetes.client.api.core_v1_api import CoreV1Api

from app.core.permission import check_permission
import app.kubernetes.pod as k8s_pod

from app.models.user import User
from app.models.route import RoleEnum, RouteItem

dash_board_route = RouteItem(**{
    'path': '/dashboard',
    'name': 'Dashboard',
    'component': 'LAYOUT',
    'redirect': '/dashboard/overview',
    'meta': {
        "title": 'routes.dashboard.dashboard',
        "icon": 'bx:bx-home',
    },
    "children": [
        {
            'path': 'overview',
            'name': 'namespaceOverview',
            'meta': {
                'title': 'routes.dashboard.overview'
            }
        }
    ]
})

container_route = RouteItem(**{
    'path': '/container',
    'name': 'Container',
    'component': 'LAYOUT',
    'redirect': '/container/overview',
    'meta': {
        'icon': 'simple-icons:kubernetes',
        'title': 'routes.container.container'
    },
    'children': [
        {
            'path': 'overview',
            'name': 'containerOverview',
            'component': '/container/overview/index',
            'meta': {
                'title': 'routes.container.overview'
            },
        },
        {
            'path': 'create',
            'name': 'containerCreate',
            'component': '/container/create/index',
            'meta': {
                'title': 'routes.container.create'
            },
        },
    ]
})

containers_route = RouteItem(**{
    'path': 'containers',
    'name': 'containers',
    'meta': {
        'title': 'routes.container.containers'
    },
})

def getMenuListByUser(user: User, core_v1_api: CoreV1Api) -> List[RouteItem]:
    if(check_permission(user.roles, RoleEnum.USER)):
        dash_board_route.children[0].component = "/dashboard/namespaceOverview/index"

        body = k8s_pod.get_pods(core_v1_api=core_v1_api, namespace=str(user.id))
        pods = [item.metadata.name for item in body.items]

        if pods != [] and not next((True for children in container_route.children if children.name == 'containers'), False):
            containers_route.redirect = f"/containers/{pods[0]}"
            containers_route.children = []
            
            for pod in pods:
                containers_route.children.append(RouteItem(**{
                    'path': pod,
                    'name': f'containers{pod.capitalize()}',
                    'component': '/container/containers/index',
                    'props': {
                        'pod_name': pod,
                    },
                    'meta': {
                        'title': pod
                    },
                }))
            
            container_route.children.append(containers_route)
        
        return([dash_board_route, container_route])
        
