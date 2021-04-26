from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from enum import Enum


class RoleEnum(str, Enum):
    #   super admin
    SUPER = 'super'

    # tester
    TEST = 'test'

    USER = 'user'


class RouteMeta(BaseModel):
    #  title
    title: str
    # Whether to ignore permissions
    ignoreAuth: Optional[bool]
    # role info
    roles: Optional[List[RoleEnum]]
    # Whether not to cache
    ignoreKeepAlive: Optional[bool]
    # Is it fixed on tab
    affix: Optional[bool]
    # icon on tab
    icon: Optional[str]

    frameSrc: Optional[str]

    # current page transition
    transitionName: Optional[str]

    # Whether the route has been dynamically added
    hideBreadcrumb: Optional[bool]

    # Hide submenu
    hideChildrenInMenu: Optional[bool]

    # Carrying parameters
    carryParam: Optional[bool]

    # Used internally to mark single-level menus
    single: Optional[bool]

    # Currently active menu
    currentActiveMenu: Optional[str]

    # Never show in tab
    hideTab: Optional[bool]

    # Never show in menu
    hideMenu: Optional[bool]

    isLink: Optional[bool]

class Recordable(BaseModel):
    __root__: Dict[str, str]


class RouteItem(BaseModel):
    path: str
    component: Any
    meta: RouteMeta
    name: Optional[str]
    props: Optional[Recordable];
    alias: Optional[Union[str, List[str]]]
    redirect: Optional[str]
    caseSensitive: Optional[bool]
    children: Optional[List[RouteItem]]

RouteItem.update_forward_refs()