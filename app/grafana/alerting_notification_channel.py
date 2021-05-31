from app.models.user import User
from app.core.config import GRAFANA_API_KEY, GRAFANA_SERVER
import requests

headers = {'Authorization': f"Bearer {GRAFANA_API_KEY}", 'Content-Type': 'application/json'}

def get_alert_channels():
    return requests.get(f"{GRAFANA_SERVER}/api/alert-notifications", headers=headers)

def get_alert_channel_by_uid(uid: str):
    return requests.get(f"{GRAFANA_SERVER}/api/alert-notifications/uid/{uid}", headers=headers)

def create_alert_channel(json: dict):
    return requests.post(f"{GRAFANA_SERVER}/api/alert-notifications", json=json, headers=headers)

def update_alert_channel_by_uid(uid:str, json: dict):
    return requests.put(f"{GRAFANA_SERVER}/api/alert-notifications/uid/{uid}", json=json, headers=headers)

def delete_alert_channel_by_uid(uid: str):
    return requests.delete(f"{GRAFANA_SERVER}/api/alert-notifications/uid/{uid}", headers=headers)

def generate_alert_channel_template(user: User):
    return {
        "uid": str(user.id),
        "name": user.realName,
        "type":  "email",
        "isDefault": False,
        "sendReminder": False,
        "disableResolveMessage": True,
        "settings": {
            "addresses": f"{user.email}",
            "uploadImage": False
        }
    }
