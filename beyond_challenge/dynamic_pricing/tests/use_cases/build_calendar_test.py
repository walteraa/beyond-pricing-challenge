from datetime import datetime, timedelta
from dynamic_pricing.utils.time import seconds_until_end_of_today
import pytest
from dynamic_pricing.use_cases.build_calendar import BuildCalendar
from dynamic_pricing.use_cases.convert_calendar import ConvertCalendar
from dynamic_pricing.use_cases.get_price_base_on_rule import GetPriceBaseOnRule
from django.core.cache import cache


@pytest.mark.freeze_time(datetime.now())
@pytest.mark.django_db
def test_when_not_cached_hasnt_currency(mocker, valid_listing):
    mocker.patch.object(cache, "get", return_value=None)
    mocker.patch.object(cache, "set")
    mocker.patch.object(GetPriceBaseOnRule, "call", return_value=13)
    mocker.patch.object(ConvertCalendar, "call")

    result = BuildCalendar.call(valid_listing)

    assert all(x == 13 for x in list(map(lambda x: x["price"], result)))
    assert len(result) == 365

    assert result[0]["date"] == datetime.now().strftime("%Y-%m-%d")
    assert result[len(result) - 1]["date"] == (
        datetime.now() + timedelta(days=len(result) - 1)
    ).strftime("%Y-%m-%d")

    cache.get.assert_called_once_with(f"{str(valid_listing.id)}_calendar")
    assert len(GetPriceBaseOnRule.call.call_args_list) == 365
    cache.set.assert_called_once_with(
        f"{str(valid_listing.id)}_calendar",
        result,
        timeout=seconds_until_end_of_today(),
    )
    ConvertCalendar.call.assert_not_called()


@pytest.mark.django_db
def test_when_cached_has_currency(mocker, valid_listing):
    some_data = "some_data"
    mocker.patch.object(cache, "get", return_value=some_data)
    mocker.patch.object(cache, "set")
    mocker.patch.object(ConvertCalendar, "call")
    mocker.patch.object(GetPriceBaseOnRule, "call")

    BuildCalendar.call(valid_listing, "BRL")

    ConvertCalendar.call.assert_called_once_with(
        valid_listing.currency, "BRL", some_data
    )
    cache.set.assert_not_called()
    GetPriceBaseOnRule.call.assert_not_called()
