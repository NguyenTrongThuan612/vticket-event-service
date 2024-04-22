from django.db import models
from django.core.validators import MinValueValidator

from vticket_app.models.event import Event
from vticket_app.enums.discount_type_enum import DiscountTypeEnum

class Promotion(models.Model):
    class Meta:
        db_table = "promotion"

    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="promotions")
    discount_type = models.CharField(max_length=100, choices=DiscountTypeEnum.choices)
    discount_value = models.IntegerField(validators=[MinValueValidator(1)])
    maximum_reduction_amount = models.IntegerField(validators=[MinValueValidator(1)])
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)
    deleted_at = models.DateField(null=True, default=None)