import dataclasses
from vticket_app.models.support_response import SupportResponse
from vticket_app.dtos.create_support_response_dto import CreateSupportResponseDto
from vticket_app.serializers.support_response_serializer import SupportResponseSerializer
class SupportResponseService:

    def create_response(self, support_response: CreateSupportResponseDto) -> bool:
        _data = dataclasses.asdict(support_response)
        instance = SupportResponse(**_data)
        instance.save()
        
        return instance.id is not None
    