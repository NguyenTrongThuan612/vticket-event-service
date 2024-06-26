from django.db import models

class EventTopic(models.Model):
    class Meta:
        db_table = "event_topic"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    description = models.TextField()
    symbolic_image_url = models.URLField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)