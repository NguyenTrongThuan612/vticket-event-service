from rest_framework.routers import SimpleRouter

from vticket_app.views.init_page_view import InitPageView

router = SimpleRouter(False)
router.register("client-page", InitPageView, "client-page")
urls = router.urls