from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse

from datetime import datetime


def create_aliased_response(model: BaseModel) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(model, by_alias=True))

def get_utcnow() -> datetime:
    return datetime.utcnow().replace(microsecond=0)