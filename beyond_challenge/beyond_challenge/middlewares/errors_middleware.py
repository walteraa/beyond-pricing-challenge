from django.core.exceptions import ValidationError
from django.urls.exceptions import Http404
from rest_framework.response import Response
from rest_framework.views import status
from dynamic_pricing.services.open_exchange.errors.invalid_currency_error import InvalidCurrencyError
from dynamic_pricing.services.open_exchange.errors.integration_error import (
    IntegrationError,
)
from rest_framework.renderers import JSONRenderer


class ErrorsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        try:
            response = self.get_response(request)
            if response.status_code == 404:
                response = Response({"message": "Not found"},
                                    status=status.HTTP_404_NOT_FOUND,
                                    content_type="application/json")
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
        except Exception:
            response = Response({"message": "Internal error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        return response
    

    def process_exception(self, _, e):
        if isinstance(e, InvalidCurrencyError):
            response = Response({"message": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(e, IntegrationError):
            response = Response({"message": e.args[0]}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        elif isinstance(e, ValidationError):
            response = Response({"errors": e.message_dict}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            breakpoint()
            response = Response({"message": "Internal error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        
        return response
        
