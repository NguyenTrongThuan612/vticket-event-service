from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from vticket_app.models.event import Event

class Feedback(models.Model):
    class Meta:
        db_table = "feedback"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    rating_score = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    submited_at = models.DateTimeField(null=False, auto_now_add=True)
    owner_id = models.IntegerField(null=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="feedbacks")