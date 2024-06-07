import os
from celery import Celery

# celery -A vticket worker -l info --autoscale 3,10

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vticket.settings')

app = Celery('vticket')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.task_default_queue = 'event_task_queue'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    pass