import dataclasses

from vticket_app.models.event import Event
from vticket_app.models.ticket_type import TicketType
from vticket_app.models.ticket_type_detail import TicketTypeDetail
from vticket_app.models.seat_configuration import SeatConfiguration

from vticket_app.dtos.ticket_type_dto import TicketTypeDto
from vticket_app.dtos.ticket_type_detail_dto import TicketTypeDetailDto
from vticket_app.dtos.seat_configuration_dto import SeatConfigurationDto

class TicketService():
    def create_ticket_types(self, dataset: list[TicketTypeDto], event: Event) -> bool:
        try:
            for data in dataset:
                _details = data.ticket_type_detail
                _seats = data.seat_configuration
                
                _data = dataclasses.asdict(data)
                _data.pop("ticket_type_detail")
                _data.pop("seat_configuration")

                instance = TicketType.objects.create(event=event, **_data)
                result = (
                    bool(instance.id)
                    and self.config_seats(_seats, instance)
                    and self.create_ticket_type_details(_details, instance)
                )
                
                if not result:
                    return False
                
            return True
        except Exception as e:
            print(e)
            return False
        
    def create_ticket_type_details(self, dataset: list[TicketTypeDetailDto], ticket_type: TicketType):
        try:
            instances = TicketTypeDetail.objects.bulk_create(
                [
                    TicketTypeDetail(
                        ticket_type=ticket_type, 
                        **dataclasses.asdict(data)
                    ) 
                    for data in dataset
                ]
            )
            return all(bool(instance.id) for instance in instances)
        except Exception as e:
            print(e)
            return False
        
    def config_seats(self, dataset: list[SeatConfigurationDto], ticket_type: TicketType) -> bool:
        try:
            instances = []

            for data in dataset:
                for seat_number in range(data.start_seat_number, data.end_seat_number):
                    instances.append(
                        SeatConfiguration(
                            ticket_type=ticket_type,
                            position=data.position,
                            seat_number=seat_number
                        )
                    )
            SeatConfiguration.objects.bulk_create(instances)
            
            return all(bool(instance.id) for instance in instances)
        except Exception as e:
            print(e)
            return False