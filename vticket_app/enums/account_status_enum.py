from django.db.models import TextChoices

class AccountStatusEnum(TextChoices):
    ACTIVED = "ACTIVED"
    UNVERIFIED = "UNVERIFIED"
    BLOCKED = "BLOCKED"