from datetime import date
from dataclasses import dataclass

@dataclass
class CreateFeedbackDto():
    title: str = None
    content: str = None
    rating_score: int = None
    submited_at: date = None
    owner_id: int = None
    event: int = None