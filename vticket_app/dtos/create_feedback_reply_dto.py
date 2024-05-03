from datetime import date
from dataclasses import dataclass

@dataclass
class CreateFeedbackReplyDto():
    content: str = None
    replied_at: date = None
    owner_id: int = None
    feedback: int = None