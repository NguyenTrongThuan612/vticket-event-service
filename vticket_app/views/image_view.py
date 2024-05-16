from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from vticket_app.helpers.swagger_provider import SwaggerProvider
from vticket_app.helpers.image_storage_providers.image_storage_provider import ImageStorageProvider
from vticket_app.helpers.image_storage_providers.firebase_storage_provider import FirebaseStorageProvider

from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.validations.image_validator import ImageValidator

class ImageView(viewsets.ViewSet):
    image_storage_provider: ImageStorageProvider = FirebaseStorageProvider()
    parser_classes = (MultiPartParser,)    
        
    @swagger_auto_schema(
        manual_parameters=[
            SwaggerProvider.header_authentication(),
            SwaggerProvider.form_data("image", openapi.TYPE_FILE)
        ]
    )
    @validate_body(ImageValidator)
    def create(self, request: Request, validated_body):
        try:
            url = self.image_storage_provider.upload_image(validated_body["image"])
            return RestResponse().success().set_data({"url": url}).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response