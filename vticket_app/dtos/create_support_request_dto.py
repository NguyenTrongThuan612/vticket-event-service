from datetime import date
from dataclasses import dataclass

@dataclass
class CreateSupportRequestDto():
    title: str = None
    content: str = None
    submited_at: date = None
    owner_id: int = None
    event: int = None