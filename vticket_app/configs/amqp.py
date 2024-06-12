import pika
from django.conf import settings

__amqp_conn = pika.BlockingConnection(pika.URLParameters(settings.AMQP_URL))
log_channel = __amqp_conn.channel()
log_channel.queue_declare(queue='system_log')