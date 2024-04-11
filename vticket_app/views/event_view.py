from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema

from vticket_app.serializers.event_serializer import EventSerializer
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body

class EventView(viewsets.ViewSet):
    authentication_classes = ()

    @validate_body(EventSerializer)
    @swagger_auto_schema(request_body=EventSerializer)
    def create(self, request, validated_body):
        try:
            pass
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response