from typing import TypedDict, Literal

CARRIER_OPTIONS = Literal["att", "tmobile", "verizon", "sprint"]

class NotificationReceiver(TypedDict):
    phone_number: str
    carrier: CARRIER_OPTIONS
