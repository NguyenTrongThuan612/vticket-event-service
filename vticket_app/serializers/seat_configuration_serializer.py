from rest_framework import serializers
from django.core.cache import cache

from vticket_app.models.seat_configuration import SeatConfiguration

class SeatConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatConfiguration
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(existing - fields):
            self.fields.pop(field, None)

    def to_representation(self, instance: SeatConfiguration):
        re = super().to_representation(instance)
        is_not_available = (
            instance.user_tickets.filter(is_refunded=False).exists()
            or bool(cache.keys(f"booking:*:seat:{instance.id}"))
        )
        return {**re, "is_not_available": is_not_available}