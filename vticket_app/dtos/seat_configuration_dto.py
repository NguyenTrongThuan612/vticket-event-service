from dataclasses import dataclass

@dataclass
class SeatConfigurationDto():
    position: str = None
    seat_number: int = None