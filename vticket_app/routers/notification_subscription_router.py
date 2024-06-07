from rest_framework.routers import SimpleRouter

from vticket_app.views.notification_subscription_view import NotificationSubscriptionView

router = SimpleRouter(False)
router.register("subcription", NotificationSubscriptionView, "subcription")
urls = router.urls