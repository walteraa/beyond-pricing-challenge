import pytest
from dynamic_pricing.models.market import Market
from dynamic_pricing.use_cases.get_or_create_market import GetOrCreateMarket


@pytest.mark.django_db
def test_when_created():
    previous_count = Market.objects.count()

    GetOrCreateMarket.call("new-market")

    assert Market.objects.count() == previous_count + 1


@pytest.mark.django_db
def test_when_get(persisted_market):
    previous_count = Market.objects.count()

    GetOrCreateMarket.call(persisted_market.label)

    assert Market.objects.count() == previous_count
