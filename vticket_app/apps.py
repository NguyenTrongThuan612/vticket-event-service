from django.apps import AppConfig
import threading


keep_app_alive_thread = threading.Thread()
keep_app_alive_thread.start()

class VticketAccountServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vticket_app'
    app_version = 'v1'
    app_route = 'vticket-event-service'
    api_prefix = f"apis/{app_route}/{app_version}/"