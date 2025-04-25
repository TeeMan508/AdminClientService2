import logging

import requests
from celery import shared_task
from celery.signals import setup_logging

from worker.logger import correlation_id_ctx, logger, LOGGING_CONFIG


@setup_logging.connect
def receiver_setup_logging(loglevel, logfile, format, colorize, **kwargs):  # pragma: no cover
    logging.config.dictConfig(LOGGING_CONFIG)

@shared_task()
def send_message(tg_id: str, msg: str, cor_id: str):
    correlation_id_ctx.set(cor_id)

    logger.info("Sending send_message request to bot")
    response = requests.post("http://bot:8050/tg/send_message",
                             json={"tg_id": tg_id, "msg": msg},
                             headers={"X-CORRELATION-ID": cor_id})

    response.raise_for_status()

