from os import getenv
from typing import Optional
import requests


def send_notification(message: str, to_admin: bool = False, ticker: Optional[str] = None):

    token = getenv("PUSHOVER_API_KEY")
    if to_admin:
        user = getenv("PUSHOVER_ADMIN_ID")
    else:
        user = getenv("PUSHOVER_GROUP_ID")
    
    
        # message += "https://finance.yahoo.com/quote/" + ticker

    body = {
        "token": token,
        "user": user,
        "message": message
    }
    if ticker is not None:
        body["url"] = "https://finance.yahoo.com/quote/" + ticker
    requests.post("https://api.pushover.net/1/messages.json", json=body)

