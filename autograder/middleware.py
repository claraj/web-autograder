import json
from django.http import HttpResponseBadRequest


class HelloMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # do stuff here

        print("middleware here")

        if request.method == 'PUT' and request.content_type == 'application/json':
            try:

                print('json body')

                print(request.body)
                request.JSON = json.loads(request.body)
                print(request.JSON)
            except ValueError as ve:
                return HttpResponseBadRequest('Unable to parse JSON')



        return response
