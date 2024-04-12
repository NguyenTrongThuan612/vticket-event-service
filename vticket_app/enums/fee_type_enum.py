from django.db import models

class FeeTypeEnum(models.TextChoices):
    percent = "percent"
    cash = "cash"