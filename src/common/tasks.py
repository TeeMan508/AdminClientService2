import time

from celery import shared_task

@shared_task()
def tmp_task():
    time.sleep(3)
    return "task_completed"