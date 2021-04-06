from typing import List, Optional

from pydantic import EmailStr
from pydantic.main import BaseModel

from app.models.dbmodel import DBModelMixin
from app.models.rwmodel import MongoModel, OID
from app.core.security import generate_salt, get_password_hash, verify_password

class UserRole(BaseModel):
    roleName: str
    value: str

class UserBase(MongoModel):
    email: EmailStr
    realName: str = ""
    desc: Optional[str] = ""
    roles: List[UserRole]


class UserInDB(DBModelMixin, UserBase):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)

    def change_permission(self, permission: str):
        self.permission = permission

class User(UserBase):
    token: str
    id: OID

class UserInResponse(MongoModel):
    user: User


class UserInLogin(MongoModel):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    realName: str
    desc: Optional[str] = ""
    roles: Optional[List[UserRole]] = [{"roleName": "User", "value": "user"}]


class UserInUpdate(MongoModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    realName: Optional[str] = None
    desc: Optional[str] = None
