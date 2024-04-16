from django.db.models import TextChoices

class DiscountTypeEnum(TextChoices):
    total_bill = "total_bill"