from vticket_app.configs.amqp import publisher

class RequestLogLayer:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            publisher.publish(request.__dict__)
            response = self.get_response(request)
            publisher.publish(response.__dict__)
        except Exception as e:
            print(e)
        else:
            return response