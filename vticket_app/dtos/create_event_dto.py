from datetime import date, time
from dataclasses import dataclass

from vticket_app.models.event_topic import EventTopic
from vticket_app.dtos.ticket_type_dto import TicketTypeDto

@dataclass
class CreateEventDto():
    name: str = None
    description: str = None
    start_date: date = None
    end_date: date = None
    start_time: time = None
    location: str = None
    banner_url: str = None
    event_topics: list[EventTopic] = None
    ticket_types: list[TicketTypeDto] = None
    owner_id: int = None

    def __post_init__(self):
        self.ticket_types = [TicketTypeDto(**ticket_type) for ticket_type in self.ticket_types]