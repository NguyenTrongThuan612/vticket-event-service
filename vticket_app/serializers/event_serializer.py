from rest_framework import serializers

from vticket_app.models.event import Event
from vticket_app.serializers.ticket_type_serializer import TicketTypeSerializer

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ["owner_id"]

    ticket_type = TicketTypeSerializer(many=True, allow_empty=False, min_length=1, exclude=["event_id"])

    def validate(self, attrs):
        _validated_data = super().validate(attrs)

        if _validated_data["start_date"] > _validated_data["end_date"]:
            raise serializers.ValidationError("The start date must be equal to or less than the end date")
        
        return _validated_data