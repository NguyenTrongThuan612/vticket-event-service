import dataclasses

from vticket_app.dtos.user_dto import UserDTO
from vticket_app.models.feedback import Feedback
from vticket_app.dtos.create_feedback_dto import CreateFeedbackDto
from vticket_app.serializers.feedback_serializer import FeedbackSerializer

class FeedbackService:
    def create_feedback(self, feedback: CreateFeedbackDto) -> bool:
        _data = dataclasses.asdict(feedback)
        instance = Feedback(**_data)
        instance.save()
        
        return instance.id is not None
    
    def get_all_feedback(self, user_id) -> list:
        queryset = Feedback.objects.filter(owner_id=user_id)
        
        return FeedbackSerializer(queryset, many=True).data
    
    def get_feedback_by_id(self, feedback_id: int) -> Feedback:
        try:
            return Feedback.objects.get(id=feedback_id)
        except:
            return None

    def can_reply(self, feedback: Feedback, user: UserDTO) -> bool:
        return feedback.event.owner_id == user.id