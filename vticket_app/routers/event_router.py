from rest_framework.routers import SimpleRouter

from vticket_app.views.event_view import EventView

router = SimpleRouter(False)
router.register("event", EventView, "event")
urls = router.urls