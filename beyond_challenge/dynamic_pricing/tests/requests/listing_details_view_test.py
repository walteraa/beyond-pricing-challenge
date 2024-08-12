from uuid import uuid4
from django.utils.translation import Decimal
from rest_framework.views import status
from dynamic_pricing.models.rule import Rule
from dynamic_pricing.services.open_exchange.client import OpenExchangeClient
import pytest
from datetime import datetime, timedelta
from django.core.cache import cache
import requests_mock


@pytest.mark.django_db
def test_successfully_when_not_passing_currency(client, list_of_listings):
    listing = list_of_listings[0]

    response = client.get(f"/listings/{str(listing.id)}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(listing.id)
    assert response.json()["title"] == listing.title
    assert response.json()["market"] == listing.market.label
    assert Decimal(response.json()["base_price"]) == listing.base_price
    assert response.json()["currency"] == listing.currency

    calendar = response.json()["calendar"]
    base_price = response.json()["base_price"]

    for day in calendar:
        week_day_index = datetime.strptime(day["date"], "%Y-%m-%d").weekday()
        week_day_value = Rule.DaysOfWeek.choices()[week_day_index][0]
        rule = listing.market.rules.filter(day_of_week=week_day_value).first()

        if rule:
            assert Decimal(base_price) * rule.multiplier == Decimal(day["price"])
        else:
            assert Decimal(base_price) == Decimal(day["price"])

    assert calendar[0]["date"] == datetime.now().strftime("%Y-%m-%d")
    assert calendar[len(calendar) - 1]["date"] == (
        datetime.now() + timedelta(days=len(calendar) - 1)
    ).strftime("%Y-%m-%d")


@pytest.mark.django_db
def test_successfully_when_source_usd_and_passing_another_currency(
    mocker, client, list_of_listings
):
    listing = list_of_listings[0]
    mocked_exchange_rate = 13
    mocker.patch.object(
        OpenExchangeClient, "latest_rate", return_value=mocked_exchange_rate
    )
    mocker.patch.object(cache, "get", return_value=None)

    response = client.get(f"/listings/{str(listing.id)}?currency=BRL")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(listing.id)
    assert response.json()["title"] == listing.title
    assert response.json()["market"] == listing.market.label
    assert Decimal(response.json()["base_price"]) == listing.base_price
    assert response.json()["currency"] == listing.currency

    base_price = response.json()["base_price"]
    calendar = response.json()["calendar"]

    for day in calendar:
        week_day_index = datetime.strptime(day["date"], "%Y-%m-%d").weekday()
        week_day_value = Rule.DaysOfWeek.choices()[week_day_index][0]
        rule = listing.market.rules.filter(day_of_week=week_day_value).first()

        if rule:
            assert (
                Decimal(base_price) * Decimal(rule.multiplier)
            ) * mocked_exchange_rate == Decimal(day["price"])
        else:
            assert Decimal(base_price) * mocked_exchange_rate == Decimal(day["price"])

    assert calendar[0]["date"] == datetime.now().strftime("%Y-%m-%d")
    assert calendar[len(calendar) - 1]["date"] == (
        datetime.now() + timedelta(days=len(calendar) - 1)
    ).strftime("%Y-%m-%d")


@pytest.mark.django_db
def test_successfully_when_source_not_usd_and_passing_currency(
    mocker, client, list_of_listings
):
    listing = list_of_listings[0]
    listing.currency = "EUR"
    listing.save()
    mocked_rates = {"rates": {"EUR": 2, "BRL": 3}}

    mocker.patch.object(cache, "get", return_value=None)
    with requests_mock.Mocker() as mock_request:
        mock_request.get(
            f"{OpenExchangeClient().BASE_URL}/latest.json?app_id={OpenExchangeClient().APP_ID}",
            json=mocked_rates,
        )
        response = client.get(f"/listings/{str(listing.id)}?currency=BRL")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == str(listing.id)
        assert response.json()["title"] == listing.title
        assert response.json()["market"] == listing.market.label
        assert Decimal(response.json()["base_price"]) == listing.base_price
        assert response.json()["currency"] == listing.currency

        base_price = response.json()["base_price"]
        calendar = response.json()["calendar"]

        for day in calendar:
            week_day_index = datetime.strptime(day["date"], "%Y-%m-%d").weekday()
            week_day_value = Rule.DaysOfWeek.choices()[week_day_index][0]
            rule = listing.market.rules.filter(day_of_week=week_day_value).first()

            if rule:
                assert (
                    (Decimal(base_price) * Decimal(rule.multiplier))
                    / mocked_rates["rates"]["EUR"]
                ) * mocked_rates["rates"]["BRL"] == Decimal(day["price"])
            else:
                assert (
                    Decimal(base_price) / mocked_rates["rates"]["EUR"]
                ) * mocked_rates["rates"]["BRL"] == Decimal(day["price"])

        assert calendar[0]["date"] == datetime.now().strftime("%Y-%m-%d")
        assert calendar[len(calendar) - 1]["date"] == (
            datetime.now() + timedelta(days=len(calendar) - 1)
        ).strftime("%Y-%m-%d")


@pytest.mark.django_db
def test_fail_due_to_wrong_currency(mocker, client, list_of_listings):
    listing = list_of_listings[0]
    listing.currency = "EUR"
    listing.save()
    mocked_rates = {"rates": {"EUR": 2, "BRL": 3}}

    mocker.patch.object(cache, "get", return_value=None)
    with requests_mock.Mocker() as mock_request:
        mock_request.get(
            f"{OpenExchangeClient().BASE_URL}/latest.json?app_id={OpenExchangeClient().APP_ID}",
            json=mocked_rates,
        )
        response = client.get(f"/listings/{str(listing.id)}?currency=AAA")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"message": "AAA is not a valid currency"}


@pytest.mark.django_db
def test_fail_due_to_not_found(client):
    response = client.get(f"/listings/{str(uuid4())}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"message": "Not found"}
