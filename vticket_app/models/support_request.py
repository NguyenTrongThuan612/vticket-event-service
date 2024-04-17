from django.db import models
from vticket_app.models.event import Event

class SupportRequest(models.Model):
    class Meta:
        db_table = "support_request"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    submited_at = models.DateTimeField(null=False, auto_now_add=True)
    is_recalled = models.BooleanField(default=False)
    owner_id = models.IntegerField(null=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="support_requests")