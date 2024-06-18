from django.db.models import TextChoices

class DiscountTypeEnum(TextChoices):
    percent = "percent"
    cash = "cash"