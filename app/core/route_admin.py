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
        "title": 'routes.adminDashboard.dashboard',
        "icon": 'bx:bx-home',
    },
    "children": [
        {
            'path': 'overview',
            'name': 'nodeOverview',
            'component': '/admin/dashboard/nodeOverview',
            'meta': {
                'title': 'routes.adminDashboard.nodeOverview'
            }
        },
        {
            'path': 'ceph-overview',
            'name': 'cephOverview',
            'component': '/admin/dashboard/cephOverview',
            'meta': {
                'title': 'routes.adminDashboard.cephOverview'
            }
        }
    ]
})


terminal_route = RouteItem(**{
    'path': '/terminal',
    'name': 'Terminal',
    'component': 'LAYOUT',
    'redirect': '/terminal/ceph',
    'meta': {
        "title": 'routes.adminTerminal.terminal',
        "icon": 'bx:bx-terminal',
    },
    "children": [
        {
            'path': 'system',
            'name': 'systemTerminal',
            'component': '/admin/terminal/webTerminal',
            'props': {
                'podNamespace': 'kubezephyr',
                'podName': 'kubectl',
            },
            'meta': {
                'title': 'routes.adminTerminal.systemTerminal'
            }
        },
        {
            'path': 'ceph',
            'name': 'cephTerminal',
            'component': '/admin/terminal/webTerminal',
            'props': {
                'podNamespace': 'rook-ceph',
                'podName': 'rook-ceph-tools',
            },
            'meta': {
                'title': 'routes.adminTerminal.cephTerminal'
            }
        },
    ]
})


users_route = RouteItem(**{
    'path': '/users',
    'name': 'Users',
    'component': '/admin/users/index',
    'meta': {
        "title": 'routes.adminUsers.users',
        "icon": 'bx:bx-user',
    },
})


def generate_admin_route(user: User, core_v1_api: CoreV1Api):
    return([dashboard_route, terminal_route, users_route, ])