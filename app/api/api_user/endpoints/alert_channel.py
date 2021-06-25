from fastapi import APIRouter, Depends, HTTPException, Body
import json

from app.core.jwt import get_current_user_authorizer
from app.models.user import User
from app.models.alert_channel import AlertChannelInUpdate, AlertChannelInResponse

import app.grafana.alerting_notification_channel as alerting_notification_channel

router = APIRouter()

@router.get(
    "/alert-channel",
    response_model=AlertChannelInResponse,
    tags=["ADMIN alerting notification channels"]
)
async def get_alert_channel_by_uid(
    user: User = Depends(get_current_user_authorizer())
):
    uid = str(user.id)

    result = alerting_notification_channel.get_alert_channel_by_uid(uid)
    status_code = result.status_code
    content = json.loads(result.content)

    if(result.status_code >= 300):
        raise HTTPException(status_code=status_code, detail=content)

    return AlertChannelInResponse(**content, addresses = [address for address in content['settings']['addresses'].split(';') if address != ''])

@router.put(
    "/alert-channel",
    response_model=AlertChannelInResponse,
    tags=["alerting notification channel"]
)
async def update_alert_channel_by_uid(
    alert_channel: AlertChannelInUpdate = Body(..., embed=False),
    user: User = Depends(get_current_user_authorizer())
):
    uid = str(user.id)

    result = alerting_notification_channel.get_alert_channel_by_uid(uid)
    status_code = result.status_code
    old_alert_channel = content = json.loads(result.content)

    if(result.status_code >= 300):
        raise HTTPException(status_code=status_code, detail=content)

    content = json.loads(alerting_notification_channel.update_alert_channel_by_uid(uid, {
        'name': old_alert_channel['name'] if alert_channel.name is None else alert_channel.name,
        'type': 'email',
        'isDefault': old_alert_channel['isDefault'] if alert_channel.isDefault is None else alert_channel.isDefault,
        'sendReminder': old_alert_channel['sendReminder'] if alert_channel.sendReminder is None else alert_channel.sendReminder,
        'disableResolveMessage': old_alert_channel['disableResolveMessage'] if alert_channel.disableResolveMessage is None else alert_channel.disableResolveMessage,
        'settings': {
            'addresses': ';'.join(alert_channel.addresses) or '', 
            'uploadImage': old_alert_channel['settings']['uploadImage'] if alert_channel.uploadImage is None else alert_channel.uploadImage
        }
    }).content)

    return AlertChannelInResponse(**content, addresses = [address for address in content['settings']['addresses'].split(';') if address != ''])
