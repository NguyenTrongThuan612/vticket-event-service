from rest_framework.routers import SimpleRouter

from vticket_app.views.image_view import ImageView

router = SimpleRouter(False)
router.register("image", ImageView, "image")
urls = router.urls