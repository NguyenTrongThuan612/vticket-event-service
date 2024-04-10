from django.db.models import IntegerChoices

class GenderEnum(IntegerChoices):
    PRIVATE = -1
    FEMALE = 0
    MALE = 1