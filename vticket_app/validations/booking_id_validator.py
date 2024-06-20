from rest_framework import serializers
from django.core.cache import cache

class BookingIdValidator(serializers.Serializer):
    booking_id = serializers.CharField()

    def validate_booking_id(self, value):
        if not bool(cache.keys(f"booking:{value}:*:*")):
            raise serializers.ValidationError("invalid_booking_id")

        return value