import datetime
import dataclasses
from vticket_app.models.support_request import SupportRequest
from vticket_app.dtos.support_request_dto import SupportRequestDto

class SupportRequestService:

    def create_request(self, supportRequest: SupportRequestDto) -> bool:
        _data = dataclasses.asdict(supportRequest)

        instance = SupportRequest(**_data)
        instance.save()
        
        if instance.id is None:
            return False
        return True
    