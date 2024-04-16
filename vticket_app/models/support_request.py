from django.db import models

class SupportRequest(models.Model):
    class Meta:
        db_table = "support_request"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    submited_at = models.DateField(null=False, auto_now_add=True)
    is_recalled = models.BooleanField(default=False)
    user_id = models.IntegerField(null=False)