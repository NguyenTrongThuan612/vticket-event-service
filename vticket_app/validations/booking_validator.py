from rest_framework import serializers

from vticket_app.models.seat_configuration import SeatConfiguration
from vticket_app.models.event import Event

class BookingValidator(serializers.Serializer):
    seats = serializers.PrimaryKeyRelatedField(
        queryset=SeatConfiguration.objects.all(),
        many=True
    )
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), many=False)

    def validate(self, attrs):
        _validated_data = super().validate(attrs)

        if any(seat.ticket_type.event.id != _validated_data["event"].id for seat in _validated_data["seats"]):
            raise serializers.ValidationError("Has invalid seat' event id!")
        
        return _validated_data