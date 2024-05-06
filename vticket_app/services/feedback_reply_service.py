import dataclasses
from vticket_app.models.feedback_reply import FeedbackReply
from vticket_app.dtos.create_feedback_reply_dto import CreateFeedbackReplyDto

class FeedbackReplyService:
    def create_reply(self, feedback_reply: CreateFeedbackReplyDto) -> bool:
        _data = dataclasses.asdict(feedback_reply)
        instance = FeedbackReply(**_data)
        instance.save()
        
        return instance.id is not None