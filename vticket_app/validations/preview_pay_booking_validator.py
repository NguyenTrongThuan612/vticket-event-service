import datetime
from rest_framework import serializers

from vticket_app.models.booking import Booking
from vticket_app.models.promotion import Promotion

class PreviewPayBookingValidator(serializers.Serializer):
    booking_id = serializers.CharField()
    discount = serializers.PrimaryKeyRelatedField(queryset=Promotion.objects.filter(deleted_at=None, evaluation_field__gte=1), allow_null=True)

    def validate(self, attrs):
        try:
            _validated_data = super().validate(attrs)
            booking = Booking.objects.get(id=_validated_data["booking_id"])

            if booking.seats.all()[0].ticket_type.event.id != _validated_data["discount"].event.id:
                raise serializers.ValidationError("Can not apply the discount for this event!")
            
            return _validated_data
        except Exception as e:
            print(e)
            raise serializers.ValidationError("booking_not_found")
        
    def validate_discount(self, value: Promotion):
        _today = datetime.datetime.now().date()

        if value.start_date > _today or value.end_date < _today:
            serializers.ValidationError("expired")
            
        return value
