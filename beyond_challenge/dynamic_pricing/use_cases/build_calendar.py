from typing import Optional
from datetime import datetime, timedelta
from dynamic_pricing.models.listing import Listing
from dynamic_pricing.use_cases.convert_calendar import ConvertCalendar
from dynamic_pricing.use_cases.get_price_base_on_rule import GetPriceBaseOnRule
from django.core.cache import cache

from dynamic_pricing.utils.time import seconds_until_end_of_today


class BuildCalendar:

    @staticmethod
    def call(listing: Listing, currency: Optional[str] = None):
        cache_key = f"{str(listing.id)}_calendar"
        base_calendar = cache.get(cache_key)

        if not base_calendar:
            base_calendar = [
                {
                    "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                    "price": GetPriceBaseOnRule.call(
                        listing, (datetime.now() + timedelta(days=i)).weekday()
                    ),
                    "currency": listing.currency,
                }
                for i in range(0, 365)
            ]

            cache.set(cache_key, base_calendar, timeout=seconds_until_end_of_today())

        if currency and currency.upper() != listing.currency:
            ConvertCalendar.call(listing.currency, currency, base_calendar)

        return base_calendar
