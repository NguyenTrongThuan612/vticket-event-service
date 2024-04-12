from rest_framework import serializers

from vticket_app.models.event_topic import EventTopic

class EventTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTopic
        fields = ["name", "description"]