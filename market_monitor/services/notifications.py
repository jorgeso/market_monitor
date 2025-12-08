from os import getenv
import requests


def send_notification(message: str, to_admin: bool = False):

    token = getenv("PUSHOVER_API_KEY")
    if to_admin:
        user = getenv("PUSHOVER_ADMIN_ID")
    else:
        user = getenv("PUSHOVER_GROUP_ID")


    body = {
        "token": token,
        "user": user,
        "message": message
    }
    requests.post("https://api.pushover.net/1/messages.json", json=body)

