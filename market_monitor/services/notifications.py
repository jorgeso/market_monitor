from os import getenv
import requests



def send_notification(message: str):

    body = {
        "token": "aij1tozcnovyrr6ttvh7kj8dc7chzo",
        "user": "gaic6otasu4hvcaarbpahni3dw1az8",
        "message": message
    }
    requests.post("https://api.pushover.net/1/messages.json", json=body)

