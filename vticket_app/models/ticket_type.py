from django.db import models
from django.core.validators import MinValueValidator

from vticket_app.models.event import Event

class TicketType(models.Model):
    class Meta:
        db_table = "ticket_type"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket_types")