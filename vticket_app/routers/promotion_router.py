from rest_framework.routers import SimpleRouter

from vticket_app.views.promotion_view import PromotionView

router = SimpleRouter(False)
router.register("promotion", PromotionView, "promotion")
urls = router.urls