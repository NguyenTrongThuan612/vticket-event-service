from rest_framework.routers import SimpleRouter

from vticket_app.views.support_response_view import SupportResponseView

router = SimpleRouter(False)
router.register("support-response", SupportResponseView, "support-response")
urls = router.urls