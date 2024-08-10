from django.db.models.expressions import Decimal
from rest_framework.test import APIClient
from dynamic_pricing.models.listing import Listing
from dynamic_pricing.models.rule import Rule
import pytest
from dynamic_pricing.models.market import Market


@pytest.fixture
def invalid_market():
    return Market()


@pytest.fixture
def valid_market():
    return Market(label="paris")


@pytest.fixture
def persisted_market(valid_market):
    valid_market.save()
    return valid_market


@pytest.fixture
def invalid_rule():
    return Rule()


@pytest.fixture
def valid_rule(persisted_market):
    return Rule(
        day_of_week=Rule.DaysOfWeek.FRIDAY.name,
        multiplier=Decimal("1.25"),
        market=persisted_market,
    )


@pytest.fixture
def invalid_listing():
    return Listing()


@pytest.fixture
def valid_listing(persisted_market):
    return Listing(
        title="loft paris",
        base_price=Decimal("500"),
        market=persisted_market,
        currency="EUR",
    )


@pytest.fixture
def list_of_listings(valid_rule):
    return [
        Listing.objects.create(
            title=f"Test entry #{i}",
            base_price=Decimal(f"{100 + i}"),
            market=valid_rule.market,
            currency="USD",
            host_name=f"Host #{i}"
        )
        for i in range(50)
    ]


@pytest.fixture
def client():
    return APIClient()
