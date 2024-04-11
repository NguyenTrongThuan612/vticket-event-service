from rest_framework import serializers

from vticket_app.models.event import Event
from vticket_app.serializers.ticket_type_serializer import TicketTypeSerializer

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    ticket_type = TicketTypeSerializer(many=True, allow_empty=False, min_length=1, exclude=["event_id"])