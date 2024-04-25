from rest_framework import serializers

from vticket_app.models.promotion import Promotion

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(existing - fields):
            self.fields.pop(field, None)

    def validate(self, attrs):
        _validated_data = super().validate(attrs)

        if _validated_data["start_date"] > _validated_data["end_date"]:
            raise serializers.ValidationError("Start date must be equal to or less than end date!")
        
        return _validated_data