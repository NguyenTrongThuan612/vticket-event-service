from dataclasses import dataclass

@dataclass
class SeatConfigurationDto():
    position: str = None
    start_seat_number: int = None
    end_seat_number: int = None