import pika
from django.conf import settings

class Publisher:
    EXCHANGE=''
    ROUTING_KEY = 'system_log'

    def __init__(self):
        self._params = pika.URLParameters(settings.AMQP_URL)
        self._params.client_properties = {
            "connection_name": "event_service"
        }
        self._conn = None
        self._channel = None

    def connect(self):
        if not self._conn or self._conn.is_closed:
            self._conn = pika.BlockingConnection(self._params)
            self._channel = self._conn.channel()
            self._channel.queue_declare(queue='system_log')

    def _publish(self, msg: str):
        self._channel.basic_publish(
            exchange=self.EXCHANGE,
            routing_key=self.ROUTING_KEY,
            body=msg.encode()
        )

    def publish(self, msg):
        try:
            _msg = str(msg)
            self._publish(_msg)
        except Exception as e:
            print(e)
            self.connect()
            self._publish(_msg)

    def close(self):
        if self._conn and self._conn.is_open:
            self._conn.close()

publisher = None

if publisher is None:
    publisher = Publisher()