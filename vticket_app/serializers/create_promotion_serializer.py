from rest_framework import serializers

from vticket_app.models.promotion import Promotion
from vticket_app.serializers.promotion_condition_serializer import PromotionConditionSerializer

class CreatePromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        exclude = ["deleted_at"]

    promotion_condition = PromotionConditionSerializer(many=False, exclude=["promotion"])
        
    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(existing - fields):
            self.fields.pop(field, None)