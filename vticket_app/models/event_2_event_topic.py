from django.db import models

from vticket_app.models.event import Event
from vticket_app.models.event_topic import EventTopic

class Event2EventTopic(models.Model):
    class Meta:
        db_table = "event_ref_event_topic"

    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="events")
    event_topic = models.ForeignKey(EventTopic, on_delete=models.CASCADE, related_name="event_topics")
    deleted_at = models.DateTimeField(null=True, default=None)