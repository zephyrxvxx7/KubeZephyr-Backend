from typing import Optional

from pydantic import EmailStr, HttpUrl

from app.models.dbmodel import DBModelMixin, DateTimeModelMixin
from app.models.rwmodel import MongoModel
from app.core.security import generate_salt, get_password_hash, verify_password


class UserBase(MongoModel):
    username: str
    email: EmailStr
    bio: Optional[str] = ""
    image: Optional[HttpUrl] = None


class UserInDB(DBModelMixin, UserBase):
    salt: str = ""
    hashed_password: str = ""
    permission: str = "user"

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)

    def change_permission(self, permission: str):
        self.permission = permission

class User(DBModelMixin, UserBase):
    token: str


class UserInResponse(MongoModel):
    user: User


class UserInLogin(MongoModel):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str


class UserInUpdate(MongoModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None
