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


def generate_admin_route(user: User, core_v1_api: CoreV1Api):
    
    return([dashboard_route])