from celery import shared_task
import time
from vticket_app.helpers.email_providers.email_provider import EmailProvider

@shared_task
def async_send_email(**kwargs):
    return EmailProvider().send_html_template_email(**kwargs)