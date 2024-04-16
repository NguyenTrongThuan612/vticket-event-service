from dataclasses import dataclass

from vticket_app.dtos.ticket_type_detail_dto import TicketTypeDetailDto
from vticket_app.dtos.seat_configuration_dto import SeatConfigurationDto

@dataclass
class TicketTypeDto():
    name: str = None
    description: str = None
    price: int = None
    ticket_type_detail: TicketTypeDetailDto = None
    seat_configuration: SeatConfigurationDto = None

    def __post_init__(self):
        self.ticket_type_detail = [TicketTypeDetailDto(**detail) for detail in self.ticket_type_detail]
        self.seat_configuration = [SeatConfigurationDto(**seat) for seat in self.seat_configuration]