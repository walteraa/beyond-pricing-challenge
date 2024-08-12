import pytest
from django.utils.translation import Decimal
from dynamic_pricing.services.open_exchange.client import OpenExchangeClient
from django.core.cache import cache
import requests_mock
from dynamic_pricing.use_cases.convert_calendar import ConvertCalendar
from dynamic_pricing.services.open_exchange.errors.invalid_currency_error import (
    InvalidCurrencyError,
)


def test_convert_callendar_when_source_is_usd_and_not_cached(mocker, calendar_sample):
    cache.clear()

    initial_values = list(map(lambda x: x["price"], calendar_sample))

    mocked_exchange_rate = 10
    mocker.patch.object(
        OpenExchangeClient, "latest_rate", return_value=mocked_exchange_rate
    )
    mocker.patch.object(cache, "get", return_value=None)
    mocker.patch.object(cache, "set")

    ConvertCalendar.call(
        source_currency="USD", target_currency="BRL", calendar=calendar_sample
    )

    for i in range(len(calendar_sample)):
        assert calendar_sample[i]["price"] == initial_values[i] * mocked_exchange_rate

    assert len(cache.get.call_args_list) == len(calendar_sample)
    assert cache.get.call_args_list[0][0][0] == "USD_BRL_rate"
    assert len(cache.set.call_args_list) == len(calendar_sample)
    assert cache.set.call_args_list[0][0] == ("USD_BRL_rate", mocked_exchange_rate)


def test_convert_callendar_when_source_is_usd_and_is_cached(mocker, calendar_sample):
    cache.clear()

    initial_values = list(map(lambda x: x["price"], calendar_sample))

    mocked_exchange_rate = 10
    mocker.patch.object(cache, "get", return_value=mocked_exchange_rate)
    mocker.patch.object(cache, "set")

    ConvertCalendar.call(
        source_currency="USD", target_currency="BRL", calendar=calendar_sample
    )

    for i in range(len(calendar_sample)):
        assert calendar_sample[i]["price"] == initial_values[i] * mocked_exchange_rate

    assert len(cache.get.call_args_list) == len(calendar_sample)
    assert cache.get.call_args_list[0][0][0] == "USD_BRL_rate"
    cache.set.assert_not_called()


def test_convert_callendar_when_target_is_usd_and_not_cached(mocker, calendar_sample):
    cache.clear()

    initial_values = list(map(lambda x: x["price"], calendar_sample))

    mocked_exchange_rate = 10
    mocker.patch.object(
        OpenExchangeClient, "latest_rate", return_value=mocked_exchange_rate
    )
    mocker.patch.object(cache, "get", return_value=None)
    mocker.patch.object(cache, "set")

    ConvertCalendar.call(
        source_currency="BRL", target_currency="USD", calendar=calendar_sample
    )

    for i in range(len(calendar_sample)):
        assert calendar_sample[i]["price"] == initial_values[i] / mocked_exchange_rate

    assert len(cache.get.call_args_list) == len(calendar_sample)
    assert cache.get.call_args_list[0][0][0] == "BRL_USD_rate"
    assert len(cache.set.call_args_list) == len(calendar_sample)
    assert cache.set.call_args_list[0][0] == ("BRL_USD_rate", mocked_exchange_rate)


def test_convert_callendar_when_target_is_usd_and_is_cached(mocker, calendar_sample):
    cache.clear()

    initial_values = list(map(lambda x: x["price"], calendar_sample))

    mocked_exchange_rate = 10
    mocker.patch.object(cache, "get", return_value=mocked_exchange_rate)
    mocker.patch.object(cache, "set")

    ConvertCalendar.call(
        source_currency="BRL", target_currency="USD", calendar=calendar_sample
    )

    for i in range(len(calendar_sample)):
        assert calendar_sample[i]["price"] == initial_values[i] / mocked_exchange_rate

    assert len(cache.get.call_args_list) == len(calendar_sample)
    assert cache.get.call_args_list[0][0][0] == "BRL_USD_rate"
    cache.set.assert_not_called()


def test_convert_callendar_when_neither_target_source_are_usd(mocker, calendar_sample):
    cache.clear()

    calendar_sample = calendar_sample[:1]
    calendar_sample[0]["currency"] = "BRL"
    mocked_rates = {"rates": {"EUR": 2, "BRL": 3}}

    mocker.patch.object(cache, "get", return_value=None)
    mocker.patch.object(cache, "set")
    with requests_mock.Mocker() as mock_request:
        mock_request.get(
            f"{OpenExchangeClient().BASE_URL}/latest.json?app_id={OpenExchangeClient().APP_ID}",
            json=mocked_rates,
        )
        ConvertCalendar.call(
            source_currency=calendar_sample[0]["currency"],
            target_currency="EUR",
            calendar=calendar_sample,
        )

        assert calendar_sample[0]["price"] == Decimal("333.33")
        assert calendar_sample[0]["currency"] == "EUR"

        assert len(cache.get.call_args_list) == 2
        assert cache.get.call_args_list[0][0][0] == "USD_BRL_rate"
        assert cache.get.call_args_list[1][0][0] == "USD_EUR_rate"

        assert len(cache.set.call_args_list) == 2
        assert cache.set.call_args_list[0][0] == ("USD_BRL_rate", 3)
        assert cache.set.call_args_list[0][1] == {"timeout": 1800}
        assert cache.set.call_args_list[1][0] == ("USD_EUR_rate", 2)
        assert cache.set.call_args_list[1][1] == {"timeout": 1800}


def test_convert_when_error(mocker, calendar_sample):
    mocker.patch.object(
        OpenExchangeClient, "latest_rate", side_effect=InvalidCurrencyError()
    )

    with pytest.raises(InvalidCurrencyError):
        ConvertCalendar.call(
            source_currency="USD", target_currency="BRL", calendar=calendar_sample
        )
