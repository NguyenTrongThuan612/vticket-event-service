from drf_yasg import openapi

class SwaggerProvider():
    @staticmethod
    def header_authentication():
        return openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Authorization')
    
    @staticmethod
    def query_param(name: str, type: str = openapi.TYPE_STRING, description: str = ""):
        return openapi.Parameter(name, in_=openapi.IN_QUERY, type=type, description=description)
    
    @staticmethod
    def form_data(name: str, type: str = openapi.TYPE_STRING, description: str = ""):
        return openapi.Parameter(name, in_=openapi.IN_FORM, type=type, description=description)