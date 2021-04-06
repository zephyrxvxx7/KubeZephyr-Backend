from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.rwmodel import OID

class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")


class DBModelMixin(DateTimeModelMixin):
    id: Optional[OID] = None
