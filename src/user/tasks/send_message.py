import time
from typing import Any

import requests
from celery import shared_task


@shared_task()
def send_message(tg_id: str, msg: str):
    data = {"tg_id": tg_id, "msg": msg}
    print(data)
    response = requests.post("http://bot:8050/tg/send_message", json=data)
    response.raise_for_status()

