from django.apps import AppConfig


class VticketAccountServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vticket_app'
    app_version = 'v1'
    app_route = 'vticket-event-service'
    api_prefix = f"apis/{app_route}/{app_version}/"