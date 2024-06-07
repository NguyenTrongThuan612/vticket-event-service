import dataclasses
from django.db.models import Q

from vticket_app.models.event import Event
from vticket_app.dtos.create_event_dto import CreateEventDto
from vticket_app.models.event_2_event_topic import Event2EventTopic
from vticket_app.serializers.event_serializer import EventSerializer
from vticket_app.services.ticket_service import TicketService
from vticket_app.enums.fee_type_enum import FeeTypeEnum
from vticket_app.tasks.queue_tasks import async_send_email_to_all_users

class EventService():
    ticket_service = TicketService()

    def create_event(self, event: CreateEventDto) -> Event:
        try:
            _data = dataclasses.asdict(event)
            _ticket_types = event.ticket_types
            _event_topics = event.event_topics

            _data.pop("ticket_types")
            _data.pop("event_topics")

            instance = Event(**_data)
            instance.save()

            if instance.id is None:
                return None
            
            if not self.ticket_service.create_ticket_types(_ticket_types, instance):
                return None
            
            if not self.create_event_topics(_event_topics, instance):
                return None
            
            return instance
        except Exception as e:
            print(e)
            return None
        
    def create_event_topics(self, topics: list, event: Event) -> bool:
        try:
            e2et = []

            for topic in topics:
                e2et.append(
                    Event2EventTopic(
                        event=event,
                        event_topic=topic,
                        deleted_at=None
                    )
                )

            Event2EventTopic.objects.bulk_create(e2et)
            
            return True
        except Exception as e:
            print(e)
            return False
    
    def all(self) -> list[Event]:
        return Event.objects.all()
    
    def search_event(self, keyword: str) -> list[Event]:
        if keyword is None:
            queryset = self.all()
        else:
            queryset = Event.objects.filter(
                Q(name__icontains=keyword)
                | Q(description__icontains=keyword)
            )
            

        return EventSerializer(queryset.order_by("created_at"), many=True).data
    
    def get_value_types_enum(self) -> list:
        values = [choice.value for choice in FeeTypeEnum]
        return values
    
    def change_banner(self, event_id: int, banner_url: str) -> bool:
        try:
            instance = Event.objects.get(id=event_id)
            instance.banner_url = banner_url
            instance.save(update_fields=["banner_url"])
            
            return True
        except Exception as e:
            print(e)
            return False

    def get_event_by_id(self, event_id: int) -> Event | None:
        try:
            return Event.objects.get(id=event_id)
        except Exception as e:
            return None
        
    def send_new_event_email(self, event: Event):
        try:
            async_send_email_to_all_users.apply_async(kwargs={
                    "emails": ["ntt06012k2@gmail.com"],
                    "cc": [],
                    "subject": f"[Vticket] Chào đón sự kiện mới: {event.name}",
                    "template_name": "new_event.html",
                    "context": {
                        "name": event.name,
                        "start_date": event.start_date.strftime("%d-%m-%Y"),
                        "start_time": event.start_time.strftime("%H:%M"),
                        "event_url": f"https://vticket.netlify.app/event/{event.id}",
                        "event_banner_url": event.banner_url
                    }
                }
            )
        except Exception as e:
            print(e)
        
        
