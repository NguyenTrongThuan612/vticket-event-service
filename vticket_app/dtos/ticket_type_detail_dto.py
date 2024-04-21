from dataclasses import dataclass

@dataclass
class TicketTypeDetailDto():
    name: str = None
    description: str = None
    fee_type: str = None
    fee_value: int = None