from rest_framework import serializers

from vticket_app.models.promotion_condition import PromotionCondition

class PromotionConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionCondition
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(existing - fields):
            self.fields.pop(field, None)