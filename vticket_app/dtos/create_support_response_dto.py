from datetime import date
from dataclasses import dataclass

@dataclass
class CreateSupportResponseDto():
    content: str = None
    replied_at: date = None
    owner_id: int = None
    request: int = None