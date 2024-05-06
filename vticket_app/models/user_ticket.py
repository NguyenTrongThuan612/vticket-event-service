from django.db import models

from vticket_app.models.seat_configuration import SeatConfiguration

class UserTicket(models.Model):
    class Meta:
        db_table = "user_ticket"

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False)
    seat = models.ForeignKey(SeatConfiguration, on_delete=models.CASCADE, related_name="user_tickets")
    is_refunded = models.BooleanField(null=False)
    payment_id = models.IntegerField(null=True, default=None)
    paid_at = models.DateTimeField(null=True, default=None)