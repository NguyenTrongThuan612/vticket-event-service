from vticket_app.helpers.send_log import send_log


class RequestLogLayer:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        send_log(request.__dict__)
        response = self.get_response(request)
        send_log(response.__dict__)

        return response