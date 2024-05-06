from rest_framework.routers import SimpleRouter

from vticket_app.views.feedback_view import FeedbackView

router = SimpleRouter(False)
router.register("feedback", FeedbackView, "feedback")
urls = router.urls