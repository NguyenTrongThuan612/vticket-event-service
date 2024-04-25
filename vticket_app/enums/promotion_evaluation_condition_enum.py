from django.db import models

class PromotionEvaluationConditionEnum(models.TextChoices):
    gt = "gt"
    gte = "gte"
    lt = "lt"
    lte = "lte"