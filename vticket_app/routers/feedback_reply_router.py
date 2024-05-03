from rest_framework.routers import SimpleRouter

from vticket_app.views.feedback_reply_view import FeedbackReplyView

router = SimpleRouter(False)
router.register("feedback-reply", FeedbackReplyView, "feedback-reply")
urls = router.urls