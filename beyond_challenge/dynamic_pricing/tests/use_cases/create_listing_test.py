from django.utils.encoding import Decimal
from dynamic_pricing.models.market import Market
import pytest
from dynamic_pricing.models.listing import Listing
from dynamic_pricing.use_cases.create_listing import CreateListing

@pytest.mark.django_db
@pytest.mark.parametrize("host_name", ["Host name", None])
def test_create_successfully_non_existing_market_and_host_name_optional(host_name):
    previous_count = Listing.objects.count()
    previous_market_count = Market.objects.count()
    
    params = {
        "market": "new_market",
        "title": "Testing Listing",
        "base_price": Decimal("100"),
        "currency": "usd",
        "host_name": host_name
    }

    result = CreateListing.call(**params)

    assert Listing.objects.count() == previous_count + 1
    assert Market.objects.count() == previous_market_count + 1

    assert result.market.label == params["market"]
    assert result.title == params["title"]
    assert result.base_price == params["base_price"]
    assert result.currency == params["currency"].upper()
    assert result.host_name == params["host_name"]


@pytest.mark.django_db
@pytest.mark.parametrize("currency", [currency[0] for currency in Listing.Currency.choices()])
def test_create_successfully_existing_market(currency, persisted_market):
    previous_count = Listing.objects.count()
    previous_market_count = Market.objects.count()


    params = {
        "market": persisted_market.label,
        "title": "Testing Listing",
        "base_price": Decimal("100"),
        "currency": currency,
    }

    result = CreateListing.call(**params)

    assert Listing.objects.count() == previous_count + 1
    assert Market.objects.count() == previous_market_count

    assert result.market.label == params["market"]
    assert result.title == params["title"]
    assert result.base_price == params["base_price"]
    assert result.currency == params["currency"].upper()
