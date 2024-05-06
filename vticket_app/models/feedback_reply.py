from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from vticket_app.models.feedback import Feedback

class FeedbackReply(models.Model):
    class Meta:
        db_table = "feedback_reply"

    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=500)
    replied_at = models.DateTimeField(null=False, auto_now_add=True)
    owner_id = models.IntegerField(null=False)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name="feedback_replies")