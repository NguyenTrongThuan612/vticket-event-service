import pika
from django.conf import settings

url_params = pika.URLParameters(settings.AMQP_URL)
url_params.client_properties = {
    "connection_name": "event_service"
}
__amqp_conn = pika.BlockingConnection(url_params)
log_channel = __amqp_conn.channel()
log_channel.queue_declare(queue='system_log')