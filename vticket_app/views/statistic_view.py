from rest_framework import viewsets
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from drf_yasg import openapi

from vticket_app.services.statistic_service import StatisticService
from vticket_app.services.event_service import EventService
from vticket_app.serializers.event_statistic_serializer import EventStatisticSerialize
from vticket_app.serializers.statistic_serializer import StatisticSerializer

from vticket_app.middlewares.custom_permissions.is_business import IsBusiness
from vticket_app.middlewares.custom_permissions.is_admin import IsAdmin
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.helpers.swagger_provider import SwaggerProvider

class StatisticView(viewsets.ViewSet):
    statistic_service = StatisticService()
    event_service = EventService()

    @action(methods=["GET"], detail=True, url_path="event", permission_classes=(IsBusiness,))
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication(),
                                            SwaggerProvider.query_param("start_date", openapi.TYPE_STRING),
                                            SwaggerProvider.query_param("end_date", openapi.TYPE_STRING)])
    def get_ticket_sold_and_revenue_by_event(self, request: Request, pk: str):
        try:
            event = self.event_service.get_event_by_id(int(pk))
            if event is None:
                return RestResponse().defined_error().set_message("Sự kiện không tồn tại!").response
            
            if not self.event_service.can_view_statistic(event, request.user):
                return RestResponse().permission_denied().set_message("Bạn không có quyền xem thông kê của sự kiện này!").response
            
            start_date = request.query_params.get("start_date", None) 
            end_date = request.query_params.get("end_date", None)
            data = self.statistic_service.ticket_sold_and_revenue_by_event(event, start_date=start_date, end_date=end_date)
            
            return RestResponse().success().set_data(EventStatisticSerialize(data).data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response  
        

    @action(methods=["GET"], detail=False, url_path="admin", permission_classes=(IsAdmin,))
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication(),
                                            SwaggerProvider.query_param("start_date", openapi.TYPE_STRING),
                                            SwaggerProvider.query_param("end_date", openapi.TYPE_STRING)])
    def get_total_ticket_sold_and_revenue(self, request: Request):
        try:
            start_date = request.query_params.get("start_date", None) 
            end_date = request.query_params.get("end_date", None)
            data = self.statistic_service.total_ticket_sold_and_revenue(start_date=start_date, end_date=end_date)
            
            return RestResponse().success().set_data(StatisticSerializer(data).data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response  