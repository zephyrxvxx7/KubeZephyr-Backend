from pydantic.main import BaseModel
from app.models.rwmodel import MongoModel


class TokenPayload(MongoModel):
    username: str = ""

class Token(BaseModel):
    accsee_token: str
    token_type: str