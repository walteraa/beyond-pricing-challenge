import json
from rest_framework import status
from django.utils.encoding import Decimal
from dynamic_pricing.models.listing import Listing
from dynamic_pricing.models.market import Market
import pytest

@pytest.mark.django_db
def test_list_default_successfully(client, list_of_listings, persisted_market):
    default_response = client.get("/listings", content_type="application/json")

    assert len(default_response.json()) == 10
    
    listing = default_response.json()[9]

    assert listing.get("id") is not None
    assert listing.get("title") == "Test entry #9"
    assert listing.get("market") == persisted_market.label
    assert listing.get("base_price") == "109.00"
    assert listing.get("currency") == "USD"
    assert listing.get("host_name") == "Host #9"


@pytest.mark.django_db
def test_list_with_pagination_successfully(client, list_of_listings, persisted_market):
    limit = 5
    offset = 10

    paginated_response = client.get(f"/listings?limit={limit}&offset={offset}", content_type="application/json")
    
    assert len(paginated_response.json()) == limit 

    listing = paginated_response.json()[0]

    assert listing.get("id") is not None
    assert listing.get("title") == f"Test entry #{offset}"
    assert listing.get("market") == persisted_market.label
    assert listing.get("base_price") == str(Decimal("100.00") + Decimal(f"{offset}"))
    assert listing.get("currency") == "USD"
    assert listing.get("host_name") == f"Host #{offset}"
    
    listing = paginated_response.json()[limit - 1]
    
    assert listing.get("id") is not None
    assert listing.get("title") == f"Test entry #{offset + limit - 1}"
    assert listing.get("market") == persisted_market.label
    assert listing.get("base_price") == str(Decimal("100.00") + Decimal(f"{offset + limit - 1}"))
    assert listing.get("currency") == "USD"
    assert listing.get("host_name") == f"Host #{offset + limit - 1}"


@pytest.mark.django_db
@pytest.mark.parametrize("host_name", ["Host name", None])
def test_post_sucessfully_with_existing_market(client, host_name, persisted_market):
    params = {
        "market": persisted_market.label,
        "title": "Testing Listing",
        "base_price": str(Decimal("13.13")),
        "currency": "usd",
        "host_name": host_name
    }

    previous_market_count = Market.objects.count()

    response = client.post("/listings", data=json.dumps(params), content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED
    
    listing = response.json()

    assert listing.get("id") is not None
    assert listing.get("title") == params["title"]
    assert listing.get("market") == params["market"]
    assert listing.get("base_price") == params["base_price"]
    assert listing.get("currency") == params["currency"].upper()
    assert listing.get("host_name") == params["host_name"]

    assert Market.objects.count() == previous_market_count



@pytest.mark.django_db
@pytest.mark.parametrize("currency", [currency[0] for currency in Listing.Currency.choices()])
def test_post_sucessfully_with_non_existing_market(client, currency):
    params = {
        "market": "a-market",
        "title": "Testing Listing",
        "base_price": str(Decimal("13.13")),
        "currency": currency,
    }

    previous_market_count = Market.objects.count()

    response = client.post("/listings", data=json.dumps(params), content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED
    
    listing = response.json()

    assert listing.get("id") is not None
    assert listing.get("title") == params["title"]
    assert listing.get("market") == params["market"]
    assert listing.get("base_price") == params["base_price"]
    assert listing.get("currency") == params["currency"].upper()
    assert listing.get("host_name") is None

    assert Market.objects.count() == previous_market_count + 1
