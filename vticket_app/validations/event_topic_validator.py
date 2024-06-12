from rest_framework import serializers

from vticket_app.models.event_topic import EventTopic

class EventTopicValidator(serializers.Serializer):
    event_topic = serializers.PrimaryKeyRelatedField(queryset=EventTopic.objects.all(), many=False)