import datetime
import dataclasses
from vticket_app.models.support_request import SupportRequest
from vticket_app.dtos.create_support_request_dto import CreateSupportRequestDto
from vticket_app.serializers.support_request_serializer import SupportRequestSerializer
class SupportRequestService:

    def create_request(self, supportRequest: CreateSupportRequestDto) -> bool:
        _data = dataclasses.asdict(supportRequest)

        instance = SupportRequest(**_data)
        instance.save()
        
        if instance.id is None:
            return False
        return True
    
    def get_all_request(self, user_id) -> list:
        queryset = SupportRequest.objects.filter(owner_id = user_id)
        return SupportRequestSerializer(queryset, many=True).data
    
    
    