from rest_framework import serializers
from vticket_app.models.support_request import SupportRequest
class SupportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        exclude = ["owner_id"]

    event_name = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(existing - fields):
            self.fields.pop(field, None)

    def get_event_name(self, obj):
        return obj.event.name