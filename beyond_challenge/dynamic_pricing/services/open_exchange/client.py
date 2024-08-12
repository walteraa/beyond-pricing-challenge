import requests
from django.conf import settings

from dynamic_pricing.services.open_exchange.errors.integration_error import (
    IntegrationError,
)
from dynamic_pricing.services.open_exchange.errors.invalid_currency_error import (
    InvalidCurrencyError,
)


class OpenExchangeClient:
    BASE_URL = settings.OPEN_EXCHANGE["BASE_URL"]
    APP_ID = settings.OPEN_EXCHANGE["APP_ID"]

    """
        this only works for USD as base currency due to plan limitations
    """

    def latest_rate(self, currency: str):
        try:
            response = requests.get(f"{self.BASE_URL}/latest.json?app_id={self.APP_ID}")
        except Exception:
            raise IntegrationError("Error when integrating to OpenExchange")

        if response.status_code not in range(200, 300):
            raise IntegrationError("Error when integrating to OpenExchange")

        rate = response.json().get("rates").get(currency)

        if rate is None:
            raise InvalidCurrencyError(f"{currency} is not a valid currency")

        return rate
