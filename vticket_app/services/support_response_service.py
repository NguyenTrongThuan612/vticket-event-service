import dataclasses
from vticket_app.models.support_response import SupportResponse
from vticket_app.dtos.create_support_response_dto import CreateSupportResponseDto
from vticket_app.serializers.support_response_serializer import SupportResponseSerializer
class SupportResponseService:

    def create_response(self, supportResponse: CreateSupportResponseDto) -> bool:
        _data = dataclasses.asdict(supportResponse)
        instance = SupportResponse(**_data)
        instance.save()
        
        return instance.id is not None
    
    def get_all_response(self, user_id) -> list:
        queryset = SupportResponse.objects.filter(owner_id=user_id)
        return SupportResponseSerializer(queryset, many=True).data