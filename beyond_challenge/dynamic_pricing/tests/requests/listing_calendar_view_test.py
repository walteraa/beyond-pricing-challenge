from datetime import datetime, timedelta
from django.utils.translation import Decimal
import pytest
import requests_mock
from rest_framework.views import status
from django.core.cache import cache
from dynamic_pricing.services.open_exchange.client import OpenExchangeClient


@pytest.mark.django_db
def test_get_all_without_filter(client, valid_listing):
    valid_listing.save()

    response = client.get(f"/listings/{str(valid_listing.id)}/calendar")

    assert response.status_code == status.HTTP_200_OK
    calendar = response.json()

    assert len(calendar) == 365
    assert calendar[0]["date"] == datetime.now().strftime("%Y-%m-%d")
    assert calendar[len(calendar) - 1]["date"] == (
        datetime.now() + timedelta(days=len(calendar) - 1)
    ).strftime("%Y-%m-%d")


@pytest.mark.django_db
def test_get_filtering_only_by_start_date(client, valid_listing):
    valid_listing.save()
    start_date = (datetime.now() + timedelta(days=360)).strftime("%Y-%m-%d")

    response = client.get(
        f"/listings/{str(valid_listing.id)}/calendar?start_date={start_date}"
    )

    assert response.status_code == status.HTTP_200_OK
    calendar = response.json()

    assert len(calendar) == 5
    assert calendar[0]["date"] == start_date
    assert calendar[len(calendar) - 1]["date"] == (
        datetime.now() + timedelta(days=364)
    ).strftime("%Y-%m-%d")


@pytest.mark.django_db
def test_get_filtering_only_by_end_date(client, valid_listing):
    valid_listing.save()
    end_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")

    response = client.get(
        f"/listings/{str(valid_listing.id)}/calendar?end_date={end_date}"
    )

    assert response.status_code == status.HTTP_200_OK
    calendar = response.json()

    assert len(calendar) == 11
    assert calendar[0]["date"] == datetime.now().strftime("%Y-%m-%d")
    assert calendar[len(calendar) - 1]["date"] == end_date


@pytest.mark.django_db
def test_get_filtering_by_start_and_end_date_and_pass_currency(
    mocker, client, valid_listing
):
    valid_listing.save()

    end_date = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
    start_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

    mocked_rates = {"rates": {"EUR": 2, "BRL": 3}}

    mocker.patch.object(cache, "get", return_value=None)
    with requests_mock.Mocker() as mock_request:
        mock_request.get(
            f"{OpenExchangeClient().BASE_URL}/latest.json?app_id={OpenExchangeClient().APP_ID}",
            json=mocked_rates,
        )
        response = client.get(
            f"/listings/{str(valid_listing.id)}/calendar?start_date={start_date}&end_date={end_date}&currency=BRL"
        )

        calendar = response.json()

        assert len(calendar) == 11
        assert calendar[0]["date"] == start_date
        assert calendar[10]["date"] == end_date
        assert all(
            x == Decimal("750") for x in list(map(lambda d: d["price"], calendar))
        )
        assert all(x == "BRL" for x in list(map(lambda d: d["currency"], calendar)))
