import dataclasses
from vticket_app.models.support_request import SupportRequest
from vticket_app.dtos.create_support_request_dto import CreateSupportRequestDto
from vticket_app.serializers.support_request_serializer import SupportRequestSerializer
from vticket_app.dtos.user_dto import UserDTO

class SupportRequestService:
    def create_request(self, support_request: CreateSupportRequestDto) -> bool:
        _data = dataclasses.asdict(support_request)

        instance = SupportRequest(**_data)
        instance.save()
        
        if instance.id is None:
            return False
        return True
    
    def get_all_request(self, user_id) -> list:
        queryset = SupportRequest.objects.filter(event__owner_id=user_id)
        
        return SupportRequestSerializer(queryset, many=True).data
    
    def get_request_by_id(self, request_id: int) -> SupportRequest:
        try:
            return SupportRequest.objects.get(id=request_id)
        except:
            return None

    def can_reply(self, support_request: SupportRequest, user: UserDTO) -> bool:
        return support_request.event.owner_id == user.id
    
    