from rest_framework import serializers

class UpdateBookingValidator(serializers.Serializer):
    booking_id = serializers.CharField()
    paid_at = serializers.DateTimeField(required=False)
    payment_id = serializers.IntegerField()