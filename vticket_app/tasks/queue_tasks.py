from celery import shared_task
from vticket_app.helpers.email_providers.email_provider import EmailProvider
from vticket_app.models.notification_subscription import NotificationSubscription

@shared_task
def async_send_email(**kwargs):
    return EmailProvider().send_html_template_email(**kwargs)

@shared_task
def async_send_email_to_all_users(**kwargs):
    try:
        for e in kwargs.pop("emails", []):
            async_send_email.apply_async(kwargs={**kwargs, "to": [e]})
        
        return True
    except Exception as e:
        return e