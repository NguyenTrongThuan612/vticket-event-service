from django.db.models import TextChoices

class RoleEnum(TextChoices):
    ADMIN = "admin"
    CUSTOMER = "customer"
    BUSINESS = "business"