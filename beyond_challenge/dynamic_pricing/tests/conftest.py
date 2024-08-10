from django.db.models.expressions import Decimal
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
        title="lof paris",
        base_price=Decimal("500"),
        market=persisted_market,
        currency="EUR",
    )
