from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from vticket_app.services.notification_subscription_service import NotificationSubcriptionService
from vticket_app.utils.response import RestResponse
from vticket_app.helpers.swagger_provider import SwaggerProvider


class NotificationSubscriptionView(viewsets.ViewSet):
    ns_service = NotificationSubcriptionService()
    
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    @action(methods=["GET"], detail=False, url_path="me/status")
    def get_status(self, request: Request):
        try:
            enable = self.ns_service.get_subscription_status_by_email(request.user.email)
            return RestResponse().success().set_data({"is_enable": enable}).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    @action(methods=["GET"], detail=False, url_path="me/change-status")
    def change_status(self, request: Request):
        try:
            ok = self.ns_service.change_subscription_status_by_email(request.user.email)

            if ok:
                return RestResponse().success().response
            
            return RestResponse().defined_error().response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response