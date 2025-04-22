import time

import requests
from celery.result import AsyncResult

from bot.api.tg.check_result import TmpRequest
from bot.api.tg.send_message import MessageModelRequest
from src.api.logger import logger


def send_request_tmp(task_id: AsyncResult, client_id: int):
    # logger.info("123123123")
    # logger.info(task_id.task_id)
    asd = TmpRequest.model_validate({"task_id": task_id.task_id})
    response = requests.post("http://bot:8050/tg/check_result", json=asd.model_dump())
    logger.info(response.json())
    if response.json()['task_status'] == "SUCCESS":
        data = MessageModelRequest.model_validate({"msg": task_id.task_id, "client_id": client_id})
        requests.post("http://bot:8050/tg/send_message", json=data.model_dump())
    else:
        logger.info(response.json().get('task_status'))
        time.sleep(3)
        send_request_tmp(task_id, client_id)