from drf_yasg import openapi

class SwaggerProvider():
    @staticmethod
    def header_authentication():
        return openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Authorization')