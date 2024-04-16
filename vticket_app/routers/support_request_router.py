from rest_framework.routers import SimpleRouter

from vticket_app.views.support_request_view import SupportRequestView

router = SimpleRouter(False)
router.register("support-request", SupportRequestView, "support-request")
urls = router.urls