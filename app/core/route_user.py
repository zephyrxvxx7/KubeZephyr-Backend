import copy
from kubernetes.client import CoreV1Api

import app.kubernetes.pod as k8s_pod

from app.models.user import User
from app.models.route import RouteItem

dashboard_route = RouteItem(**{
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
            'component': '/dashboard/namespaceOverview/index',
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

volume_route = RouteItem(**{
    'path': '/volume',
    'name': 'Volume',
    'component': 'LAYOUT',
    'redirect': '/volume/overview',
    'meta': {
        'icon': 'clarity:container-volume-line',
        'title': 'routes.volume.volume'
    },
    'children': [
        {
            'path': 'overview',
            'name': 'volumeOverview',
            'component': '/volume/overview/index',
            'meta': {
                'title': 'routes.volume.overview'
            },
        },
        {
            'path': 'create',
            'name': 'volumeCreate',
            'component': '/volume/create/index',
            'meta': {
                'title': 'routes.volume.create'
            },
        },
        {
            'path': 'edit',
            'name': 'volumeEdit',
            'component': '/volume/edit/index',
            'meta': {
                'title': 'routes.volume.edit'
            },
        }
    ]
})

account_route = RouteItem(**{
    'path': '/account',
    'name': 'Account',
    'component': 'LAYOUT',
    'redirect': '/account/change-password',
    'meta': {
        "title": 'routes.account.account',
        "icon": 'mdi:card-account-details-outline',
    },
    "children": [
        {
            'path': 'change-password',
            'name': 'ChangePassword',
            'component': '/account/changePassword/index',
            'meta': {
                "title": 'routes.account.password',
                "icon": 'carbon:password',
            },
        },
        {
            'path': 'alert-channel',
            'name': 'UserAlertChannel',
            'component': '/account/alertChannel/index',
            'meta': {
                "title": 'routes.account.alertChannel',
                "icon": 'fluent:alert-on-24-regular',
            },
        },
    ]
})

def generate_containers(user: User, core_v1_api: CoreV1Api):
    namespace = str(user.id)

    body = k8s_pod.get_pods(core_v1_api=core_v1_api, namespace=namespace)
    pods = [item.metadata.name for item in body.items]

    containers_route.children = []

    if pods != []:
        for pod in pods:
            per_container_route = RouteItem(**{
                'path': pod,
                'name': f'container{pod.capitalize()}',
                'meta': {
                    'title': pod
                },
                'children': [
                    {
                        'path': 'dashboard',
                        'name': f'dashboard{pod.capitalize()}',
                        'component': '/container/containers/index',
                        'props': {
                            'podName': pod,
                        },
                        'meta': {
                            'icon': 'ic-baseline-dashboard',
                            'title': 'routes.container.dashboard',
                        },
                    },
                ]
            })

            # If the pod status is 'Running' that can use terminal and bound ingress.
            if k8s_pod.get_status(core_v1_api=core_v1_api, name=pod, namespace=namespace).phase == "Running":
                per_container_route.children.append(RouteItem(**{
                    'path': 'terminal',
                    'name': f'terminal{pod.capitalize()}',
                    'component': '/container/containers/webTerminal',
                    'props': {
                        'podName': pod,
                    },
                    'meta': {
                        'icon': 'bx:bx-terminal',
                        'title': 'routes.container.terminal',
                    },
                }))

                per_container_route.children.append(RouteItem(**{
                    'path': 'bind-domain',
                    'name': f'bindDomain{pod.capitalize()}',
                    'component': '/container/containers/bindDomain/index',
                    'props': {
                        'podName': pod,
                    },
                    'meta': {
                        'icon': 'grommet-icons:domain',
                        'title': 'routes.container.bindDomain',
                    },
                }))
            
            containers_route.children.append(per_container_route)
        
        container_route_copy = copy.deepcopy(container_route)
        container_route_copy.children.append(containers_route)
    
        return container_route_copy
    
    return container_route

def generate_user_route(user: User, core_v1_api: CoreV1Api):
    _container_route = generate_containers(user, core_v1_api)
    
    return([dashboard_route, _container_route, volume_route, account_route])