import importlib
import pkgutil
from django.urls import path, include
from django.apps import apps
from vticket_app.helpers.not_found_404_handler import not_found_404_handler

parent_module = __import__("vticket_app.routers", fromlist=[""])
package_path = parent_module.__path__[0]
child_modules = [module_name for _, module_name, _ in pkgutil.iter_modules([package_path])]

urls = []

for module in child_modules:
    urls += importlib.import_module(f"vticket_app.routers.{module}").urls

urlpatterns = [path(apps.get_app_config("vticket_app").api_prefix, include(urls))]
handler404 = not_found_404_handler