from datetime import datetime
from celery import shared_task

@shared_task
def keep_celery_alive():
    return f"keep_celery_alive: {datetime.now()}"