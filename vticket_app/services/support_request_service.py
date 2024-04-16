import datetime
from vticket_app.models.support_request import SupportRequest
from vticket_app.serializers.support_request_serializer import SupportRequestSerializer

class SupportRequestService:
    serialzier_class = SupportRequestSerializer

    def create_request(self, title: str, content: str) -> bool:
        new_request = SupportRequest.objects.create(title=title, content=content)
        return bool(new_request.id)
    