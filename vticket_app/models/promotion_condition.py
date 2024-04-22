from django.db import models
from django.core.validators import MinValueValidator

from vticket_app.models.promotion import Promotion
from vticket_app.enums.promotion_evaluation_field_enum import PromotionEvaluationFieldEnum
from vticket_app.enums.promotion_evaluation_condition_enum import PromotionEvaluationConditionEnum

class PromotionCondition(models.Model):
    class Meta:
        db_table = "promotion_condition"

    id = models.AutoField(primary_key=True)
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE, related_name="promotion_condition")
    evaluation_field = models.CharField(max_length=100, choices=PromotionEvaluationFieldEnum.choices)
    condition = models.CharField(max_length=10, choices=PromotionEvaluationConditionEnum.choices)
    value = models.IntegerField(null=False, validators=[MinValueValidator(0)])