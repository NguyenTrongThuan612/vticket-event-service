from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from vticket_app.utils.response import RestResponse
from vticket_app.services.init_page_service import InitPageService

class InitPageView(viewsets.ViewSet):
    authentication_classes = ()

    init_page_service = InitPageService()

    @action(methods=["GET"], detail=False, url_path="home")
    def home(self, request: Request):
        try:
            banners = self.init_page_service.get_banner()
            topic_types = self.init_page_service.get_topic_types()
            upcomming_events = self.init_page_service.get_upcomming_events()
            outstanding_events = self.init_page_service.get_outstanding_events()      
             
            return RestResponse().success().set_data(
                {
                    "banners": banners,
                    "outstanding_events": outstanding_events,
                    "upcoming_events": upcomming_events,
                    "topic_types": topic_types
                }
            ).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response