from rest_framework.routers import SimpleRouter

from vticket_app.views.health_view import HealthView

router = SimpleRouter(False)
router.register("health", HealthView, "health")
urls = router.urls