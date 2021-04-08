from typing import List
from fastapi import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN
)

from app.models.user import UserRole


def check_permission(roles: List[UserRole], required_role_value: str):
    result =  next((True for role in roles if role.value == required_role_value), False)

    if not result:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="The user doesn't have permission to use this method"
        )
    
    return True
