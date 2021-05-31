from typing import Optional, List
from pydantic import BaseModel, EmailStr

class AlertChannelBase(BaseModel):
    name: str
    addresses: List[EmailStr]
    isDefault: Optional[bool] = False
    sendReminder: Optional[bool] = False
    disableResolveMessage: Optional[bool] = True
    uploadImage: Optional[bool] = False

class AlertChannelInCreat(AlertChannelBase):
    pass

class AlertChannelInUpdate(BaseModel):
    name: Optional[str]
    addresses: List[EmailStr]
    isDefault: Optional[bool]
    sendReminder: Optional[bool]
    disableResolveMessage: Optional[bool]
    uploadImage: Optional[bool]

class AlertChannelInResponse(AlertChannelBase):
    uid: str

class ManyAlertChannelInResponse(BaseModel):
    alert_channel: List[AlertChannelInResponse]
