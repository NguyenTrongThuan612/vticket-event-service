from rest_framework.routers import SimpleRouter

from vticket_app.views.event_management_view import EventManagementView

router = SimpleRouter(False)
router.register("event", EventManagementView, "event")
urls = router.urls