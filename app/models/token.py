from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from app.models.rwmodel import MongoModel


class TokenPayload(MongoModel):
    email: EmailStr = ""

class Token(BaseModel):
    accsee_token: str
    token_type: str