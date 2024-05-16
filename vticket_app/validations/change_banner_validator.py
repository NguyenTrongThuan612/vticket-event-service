from rest_framework import serializers

from vticket_app.models.event import Event

class ChangeBannerValidator(serializers.Serializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), many=False)
    image = serializers.ImageField()