import dataclasses

from vticket_app.dtos.user_dto import UserDTO
from vticket_app.models.event import Event
from vticket_app.dtos.create_event_dto import CreateEventDto
from vticket_app.serializers.event_serializer import EventSerializer
from vticket_app.services.ticket_service import TicketService
from vticket_app.enums.fee_type_enum import FeeTypeEnum
from django.db.models import Q
class EventService():
    ticket_service = TicketService()

    def create_event(self, event: CreateEventDto) -> bool:
        try:
            _data = dataclasses.asdict(event)
            _ticket_types = event.ticket_types
            _event_topics = event.event_topics

            _data.pop("ticket_types")
            _data.pop("event_topics")

            instance = Event(**_data)
            instance.save()

            if instance.id is None:
                return False
            
            return self.ticket_service.create_ticket_types(_ticket_types, instance)
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
    
    def get_all_event(self, user_id: int) -> list[Event]:
        return Event.objects.filter(owner_id=user_id)
    
    def can_view_statistic(self, event: Event, user: UserDTO) -> bool:
        return event.owner_id == user.id
        
