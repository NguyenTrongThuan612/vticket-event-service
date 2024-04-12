import datetime
from vticket_app.models.event_topic import EventTopic
from vticket_app.serializers.event_topic_serializer import EventTopicSerializer

class EventTopicService():
    serializer_class = EventTopicSerializer

    def create_topic(self, name: str, description: str) -> bool:
        new_topic = EventTopic.objects.create(name=name, description=description)
        return bool(new_topic.id)
    
    def get_all_topics(self) -> list:
        queryset = EventTopic.objects.filter(deleted_at=None)
        return EventTopicSerializer(queryset, many=True).data
    
    def delete_topic(self, id: int) -> bool:
        try:
            instance = EventTopic.objects.get(id=id)
            instance.deleted_at = datetime.datetime.now()
            instance.save()
            
            return True
        except Exception as e:
            return False