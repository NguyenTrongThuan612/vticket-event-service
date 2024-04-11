from django.db import models

from vticket_app.models.event_topic import EventTopic

class Event(models.Model):
    class Meta:
        db_table = "event"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    description = models.TextField()
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    location = models.CharField(max_length=500)
    banner_url = models.URLField(null=True)
    event_topic = models.ManyToManyField(EventTopic, related_name="events", through="vticket_app.Event2EventTopic")
    creator_id = models.IntegerField(null=False)