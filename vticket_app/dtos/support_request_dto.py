from datetime import date
from dataclasses import dataclass

@dataclass
class SupportRequestDto():
    title: str = None
    content: str = None
    submited_at: date = None
    is_recalled: bool = None
    owner_id: int = None
    event: int = None
    
    def __post_init__(self):
        self.is_recalled = False