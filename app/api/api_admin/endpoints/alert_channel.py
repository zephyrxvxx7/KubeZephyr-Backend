from fastapi import APIRouter, Depends, Path, HTTPException, Response, Body
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)
import json

from app.core.jwt import get_current_user_authorizer
from app.core.permission import check_permission_with_exception
from app.models.user import User
from app.models.alert_channel import AlertChannelInCreat, AlertChannelInUpdate, AlertChannelInResponse, ManyAlertChannelInResponse
from app.models.route import RoleEnum

import app.grafana.alerting_notification_channel as alerting_notification_channel

router = APIRouter()


@router.post(
    "/alert-channel",
    response_model=AlertChannelInResponse,
    response_model_exclude_none=True,
    tags=["ADMIN alerting notification channels"],
    status_code=HTTP_201_CREATED
)
async def create_alert_channel(
    alert_channel: AlertChannelInCreat = Body(..., embed=False),
    current_user: User = Depends(get_current_user_authorizer())
):
    check_permission_with_exception(current_user.roles, RoleEnum.SUPER)

    result = alerting_notification_channel.create_alert_channel({
        'name': alert_channel.name,
        'type': 'email',
        'isDefault': alert_channel.isDefault,
        'sendReminder': alert_channel.sendReminder,
        'disableResolveMessage': alert_channel.disableResolveMessage,
        'settings': {
            'addresses': ';'.join(alert_channel.addresses), 
            'uploadImage': alert_channel.uploadImage
        }
    })
    status_code = result.status_code
    content = json.loads(result.content)

    if(result.status_code >= 300):
        raise HTTPException(status_code=status_code, detail=content)

    return AlertChannelInResponse(**content, addresses = [address for address in content['settings']['addresses'].split(';') if address != ''])


@router.get(
    "/alert-channel/{uid}",
    response_model=AlertChannelInResponse,
    tags=["ADMIN alerting notification channels"]
)
async def get_alert_channel_by_uid(
    uid: str = Path(...),
    current_user: User = Depends(get_current_user_authorizer())
):
    check_permission_with_exception(current_user.roles, RoleEnum.SUPER)

    result = alerting_notification_channel.get_alert_channel_by_uid(uid)
    status_code = result.status_code
    content = json.loads(result.content)

    if(result.status_code >= 300):
        raise HTTPException(status_code=status_code, detail=content)

    return AlertChannelInResponse(**content, addresses = [address for address in content['settings']['addresses'].split(';') if address != ''])


@router.get(
    "/alert-channel",
    response_model=ManyAlertChannelInResponse,
    tags=["ADMIN alerting notification channels"]
)
async def get_alert_channels(
    current_user: User = Depends(get_current_user_authorizer())
):
    check_permission_with_exception(current_user.roles, RoleEnum.SUPER)

    result = alerting_notification_channel.get_alert_channels()
    status_code = result.status_code
    content = json.loads(result.content)

    if(result.status_code >= 300):
        raise HTTPException(status_code=status_code, detail=content)

    return ManyAlertChannelInResponse(alert_channel=[AlertChannelInResponse(**body, addresses = [address for address in body['settings']['addresses'].split(';') if address != '']) for body in content])


@router.put(
    "/alert-channel/{uid}",
    response_model=AlertChannelInResponse,
    tags=["ADMIN Resources Quota"]
)
async def update_alert_channel_by_uid(
    uid: str = Path(...),
    alert_channel: AlertChannelInUpdate = Body(..., embed=False),
    current_user: User = Depends(get_current_user_authorizer())
):
    check_permission_with_exception(current_user.roles, RoleEnum.SUPER)

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


@router.delete(
    "/alert-channel/{uid}", 
    tags=["ADMIN alerting notification channels"],
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_alert_channel_by_uid(
    uid: str = Path(...),
    current_user: User = Depends(get_current_user_authorizer()),
):
    check_permission_with_exception(current_user.roles, RoleEnum.SUPER)
    result = alerting_notification_channel.delete_alert_channel_by_uid(uid)
    status_code = result.status_code
    content = json.loads(result.content)
    
    if(status_code != HTTP_200_OK):
        raise HTTPException(status_code=status_code, detail=content)

    return Response(status_code=HTTP_204_NO_CONTENT)
