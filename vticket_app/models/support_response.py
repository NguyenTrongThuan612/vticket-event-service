from django.db import models
from vticket_app.models.support_request import SupportRequest

class SupportResponse(models.Model):
    class Meta:
        db_table = "support_response"

    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=500)
    replied_at = models.DateTimeField(null=False, auto_now_add=True)
    owner_id = models.IntegerField(null=False)
    request = models.ForeignKey(SupportRequest, on_delete=models.CASCADE, related_name="support_reponses")