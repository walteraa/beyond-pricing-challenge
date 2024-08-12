import pytest
from dynamic_pricing.use_cases.get_price_base_on_rule import GetPriceBaseOnRule


@pytest.mark.django_db
def test_get_price_when_ruled_day(ruled_listing):

    FRIDAY_DAY_OF_WEEK = 4

    assert (
        GetPriceBaseOnRule.call(ruled_listing, FRIDAY_DAY_OF_WEEK)
        == ruled_listing.base_price * ruled_listing.market.rules.first().multiplier
    )


@pytest.mark.django_db
def test_get_price_when_not_ruled_day(ruled_listing):
    DAYS_OF_WEEK = [0, 1, 2, 3, 5, 6]

    for day in DAYS_OF_WEEK:
        assert GetPriceBaseOnRule.call(ruled_listing, day) == ruled_listing.base_price
