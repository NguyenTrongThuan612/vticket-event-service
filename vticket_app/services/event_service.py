import dataclasses

from vticket_app.models.event import Event
from vticket_app.dtos.create_event_dto import CreateEventDto
from vticket_app.services.ticket_service import TicketService

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