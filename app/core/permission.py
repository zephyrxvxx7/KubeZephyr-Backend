from fastapi import HTTPException

from starlette.status import (
    HTTP_403_FORBIDDEN
)

from app.models.user import UserInDB


def check_permission(self, user: UserInDB, required_permission: str):
    admin_group = ["user", "admin"]
    user_group = ["user"]

    if user.permission == "admin":
        return
    elif user.permission == "user":
        if required_permission in user_group:
            return
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, 
                detail="Access forbidden"
            )