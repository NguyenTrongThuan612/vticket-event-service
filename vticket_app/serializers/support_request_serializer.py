from rest_framework import serializers
from vticket_app.models.support_request import SupportRequest

class SupportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = ["title", "content"]