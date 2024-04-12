from django.db import models
from django.core.validators import MinValueValidator

from vticket_app.models.ticket_type import TicketType

class SeatConfiguration(models.Model):
    class Meta:
        db_table = "seat_configuration"

    id = models.AutoField(primary_key=True)
    position = models.CharField(max_length=100)
    seat_number = models.IntegerField(validators=[MinValueValidator(0)])
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name="seat_configurations")