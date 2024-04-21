from rest_framework import serializers
from vticket_app.models.support_response import SupportResponse
class SupportResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportResponse
        exclude = ["owner_id"]

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(existing - fields):
            self.fields.pop(field, None)