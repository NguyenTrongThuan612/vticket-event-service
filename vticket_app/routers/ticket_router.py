from rest_framework.routers import SimpleRouter

from vticket_app.views.ticket_view import TicketView

router = SimpleRouter(False)
router.register("ticket", TicketView, "ticket")
urls = router.urls