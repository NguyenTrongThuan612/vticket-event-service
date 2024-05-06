from django.db import models

from vticket_app.models.seat_configuration import SeatConfiguration

class Booking(models.Model):
    class Meta:
        db_table = "booking"
        
    id = models.UUIDField(primary_key=True)
    user_id = models.IntegerField(null=False)
    seats = models.ManyToManyField(SeatConfiguration, related_name="seats")
    created_at = models.DateTimeField(auto_now_add=True)