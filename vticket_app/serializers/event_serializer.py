from rest_framework import serializers

from vticket_app.models.event import Event
from vticket_app.serializers.ticket_type_serializer import TicketTypeSerializer
from vticket_app.models.event_topic import EventTopic

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ["owner_id"]

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(existing - fields):
            self.fields.pop(field, None)

    ticket_types = TicketTypeSerializer(many=True, allow_empty=False, min_length=1, exclude=["event"])
    event_topics = serializers.PrimaryKeyRelatedField(required=False, queryset=EventTopic.objects.all(), many=True, allow_null=True)

    def validate(self, attrs):
        _validated_data = super().validate(attrs)

        if _validated_data["start_date"] > _validated_data["end_date"]:
            raise serializers.ValidationError("The start date must be equal to or less than the end date")
        
        return _validated_data