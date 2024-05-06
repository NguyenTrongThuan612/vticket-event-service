from rest_framework import serializers

from vticket_app.models.ticket_type import TicketType
from vticket_app.serializers.ticket_type_detail_serlializer import TicketTypeDetailSerializer
from vticket_app.serializers.seat_configuration_serializer import SeatConfigurationSerializer

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(existing - fields):
            self.fields.pop(field, None)

    ticket_type_details = TicketTypeDetailSerializer(many=True, allow_empty=True, exclude=["ticket_type"])
    seat_configurations = SeatConfigurationSerializer(many=True, allow_empty=False)