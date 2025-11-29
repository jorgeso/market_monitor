from os import getenv
from typing import Dict, List
import smtplib
from market_monitor.typing.notifications import CARRIER_OPTIONS, NotificationReceiver



def send_text(to_phone: str, message: str, carrier="verizon"):

    CARRIERS: Dict[CARRIER_OPTIONS, str]= {
        "att": "@mms.att.net",
        "tmobile": "@tmomail.net",
        "verizon": "@vtext.com",
        "sprint": "@messaging.sprintpcs.com"
    }

    email = getenv("NOTIFICATIONS_EMAIL")
    password = getenv("NOTIFICATIONS_PASSWORD")
    recipient = to_phone + CARRIERS[carrier]
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
 
    server.sendmail(email, recipient, message)

def get_notification_receivers() -> List[NotificationReceiver]:

    project_path = getenv("MARKET_MONITOR_PATH")
    with open(f"{project_path}/notify_numbers", "r") as numbers_file:
        file_str = numbers_file.read()
    file_rows = [row for row in file_str.split("\n") if row.strip() != "" and row is not None] 
    receivers: List[NotificationReceiver] = []
    for row in file_rows:
        row_parts = row.split(",")
        receiver: NotificationReceiver = {
            "phone_number": row_parts[0],
            "carrier": row_parts[1]
        }
        receivers.append(receiver)
    return receivers
