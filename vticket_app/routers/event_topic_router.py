from rest_framework.routers import SimpleRouter

from vticket_app.views.event_topic_view import EventTopicView

router = SimpleRouter(False)
router.register("event-topic", EventTopicView, "event-topic")
urls = router.urls