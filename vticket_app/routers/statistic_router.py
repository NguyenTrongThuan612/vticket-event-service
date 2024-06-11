from rest_framework.routers import SimpleRouter

from vticket_app.views.statistic_view import StatisticView

router = SimpleRouter(False)
router.register("statistic", StatisticView, "statistic")
urls = router.urls