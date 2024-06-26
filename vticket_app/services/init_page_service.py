from typing import Union
from random import sample
from datetime import datetime

from django.db.models import Q, Count

from vticket_app.models.event import Event
from vticket_app.models.event_topic import EventTopic

from vticket_app.serializers.event_serializer import EventSerializer
from vticket_app.serializers.event_topic_serializer import EventTopicSerializer

class InitPageService():
    banner_length = 5
    topic_type_length = 6
    upcomming_events_length = 8
    outstanding_events_length = 6

    def get_banner(self) -> Union[list|None]:
        try:
            _today = datetime.now().date()
            queryset = Event.objects.filter(start_date__gte=_today).order_by("start_date")[:self.banner_length]

            return EventSerializer(queryset, many=True, exclude=["ticket_types"]).data
        except Exception as e:
            print(e)
            return None
        
    def get_upcomming_events(self) -> Union[list|None]:
        try:
            _today = datetime.now().date()
            queryset = Event.objects.filter(start_date__gte=_today).order_by("start_date")[:self.upcomming_events_length]

            return EventSerializer(queryset, many=True, exclude=["ticket_types"]).data
        except Exception as e:
            print(e)
            return None
        
    def get_topic_types(self) -> Union[list|None]:
        try:
            queryset = EventTopic.objects.filter(deleted_at=None)
            random_queryset = sample(list(queryset), self.topic_type_length)

            return EventTopicSerializer(random_queryset, many=True).data
        except Exception as e:
            print(e)
            return None
        
    def get_outstanding_events(self) -> Union[list | None]:
        try:
            _today = datetime.now().date()
            
            queryset = Event.objects.filter(start_date__gte=_today).annotate(
                tickets_sold=Count('ticket_types__seat_configurations__user_tickets', filter=Q(ticket_types__seat_configurations__user_tickets__is_refunded=False))
            ).order_by("-tickets_sold", "start_date")[:self.outstanding_events_length]

            return EventSerializer(queryset, many=True, exclude=["ticket_types"]).data
        except Exception as e:
            print(e)
            return None