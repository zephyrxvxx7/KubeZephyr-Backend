from kubernetes.client import CoreV1Api

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
            'path': 'cluster-alerts',
            'name': 'clusterAlerts',
            'component': '/admin/dashboard/clusterAlerts',
            'meta': {
                'title': 'routes.adminDashboard.clusterAlerts'
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

containers_route = RouteItem(**{
    'path': '/containers',
    'name': 'Containers',
    'component': '/admin/containers/index',
    'meta': {
        "title": 'routes.adminContainers.manage',
        "icon": 'simple-icons:kubernetes',
    },
})


users_route = RouteItem(**{
    'path': '/users',
    'name': 'Users',
    'component': '/admin/users/index',
    'meta': {
        "title": 'routes.adminUsers.manage',
        "icon": 'bx:bx-user',
    },
})

alert_channel_route = RouteItem(**{
    'path': '/alert-channel',
    'name': 'AlertChannel',
    'component': '/admin/alertChannel/index',
    'meta': {
        "title": 'routes.adminAlertChannel.manage',
        "icon": 'carbon:notification',
    },
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
    ]
})


def generate_admin_route(user: User, core_v1_api: CoreV1Api):
    return([dashboard_route, terminal_route, containers_route, users_route, alert_channel_route, account_route])