from dataclasses import dataclass

from vticket_app.dtos.ticket_type_detail_dto import TicketTypeDetailDto
from vticket_app.dtos.seat_configuration_dto import SeatConfigurationDto

@dataclass
class TicketTypeDto():
    name: str = None
    description: str = None
    price: int = None
    ticket_type_details: TicketTypeDetailDto = None
    seat_configurations: SeatConfigurationDto = None

    def __post_init__(self):
        self.ticket_type_details = [TicketTypeDetailDto(**detail) for detail in self.ticket_type_details]
        self.seat_configurations = [SeatConfigurationDto(**seat) for seat in self.seat_configurations]