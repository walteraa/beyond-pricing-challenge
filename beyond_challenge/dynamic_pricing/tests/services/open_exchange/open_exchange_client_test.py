from dynamic_pricing.services.open_exchange.client import OpenExchangeClient
from dynamic_pricing.services.open_exchange.errors.invalid_currency_error import (
    InvalidCurrencyError,
)
from dynamic_pricing.services.open_exchange.errors.integration_error import (
    IntegrationError,
)
import requests_mock
import pytest


def test_get_successfully():
    mocked_rates = {"rates": {"EUR": 2, "BRL": 3}}

    with requests_mock.Mocker() as mock_request:
        mock_request.get(
            f"{OpenExchangeClient().BASE_URL}/latest.json?app_id={OpenExchangeClient().APP_ID}",
            json=mocked_rates,
        )

        assert OpenExchangeClient().latest_rate("BRL") == 3
        assert OpenExchangeClient().latest_rate("EUR") == 2


def test_fail_due_to_missing_pair():
    mocked_rates = {"rates": {"EUR": 2, "BRL": 3}}

    with requests_mock.Mocker() as mock_request:
        mock_request.get(
            f"{OpenExchangeClient().BASE_URL}/latest.json?app_id={OpenExchangeClient().APP_ID}",
            json=mocked_rates,
        )

        with pytest.raises(InvalidCurrencyError, match="AAA is not a valid currency"):
            OpenExchangeClient().latest_rate("AAA")


def test_fail_due_to_integration_error():
    with requests_mock.Mocker() as mock_request:
        mock_request.get(
            f"{OpenExchangeClient().BASE_URL}/latest.json?app_id={OpenExchangeClient().APP_ID}",
            status_code=400,
        )

        with pytest.raises(IntegrationError, match="Error when integrating to OpenExchange"):
            OpenExchangeClient().latest_rate("BRL")
