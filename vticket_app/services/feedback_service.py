import dataclasses
import json

import requests

from vticket_app.configs.related_services import RelatedService
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
    
    def get_feedbacks_by_event_id(self, event_id: int) -> list:
        queryset = Feedback.objects.filter(event__id=event_id)
        ids = queryset.values_list('owner_id', flat=True)
        response = requests.post(
            url=f'{RelatedService.account}/user/list',
            headers={
                "Content-type": "application/json"
            },
            data=json.dumps(
                {
                    "ids": list(ids)
                }
            )
        )
        resp_data = response.json()

        owners = {user['id']: user for user in resp_data['data']}

        feedback_data = FeedbackSerializer(queryset, many=True).data

        for feedback in feedback_data:
            owner_id = feedback['owner_id']
            owner = owners.get(owner_id, {})
            feedback['owner_first_name'] = owner.get('first_name', '')
            feedback['owner_last_name'] = owner.get('last_name', '')
            feedback['owner_avatar_url'] = owner.get('avatar_url', '')
            
        return feedback_data
    
    def get_feedback_by_id(self, feedback_id: int) -> Feedback:
        try:
            return Feedback.objects.get(id=feedback_id)
        except:
            return None

    def can_reply(self, feedback: Feedback, user: UserDTO) -> bool:
        return feedback.event.owner_id == user.id