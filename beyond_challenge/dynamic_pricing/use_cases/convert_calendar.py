from django.utils.translation import Decimal
from dynamic_pricing.services.open_exchange.client import OpenExchangeClient
from django.core.cache import cache


class ConvertCalendar:

    @classmethod
    def call(cls, source_currency, target_currency, calendar):

        for day in calendar:
            day["currency"] = target_currency

            # This strategy is needed since the https://openexchangerates.org/api/convert is not available
            # for free-tier account, then if we have a base currency different than USD we do need to use USD as bridge.
            if source_currency == "USD":
                cls._convert_from_usd(day=day, source_currency=source_currency, target_currency=target_currency)
            elif target_currency == "USD":
                cls._convert_to_usd(day=day, source_currency=source_currency, target_currency=target_currency)
            else:
                cls._convert_from_any_to_any(day=day, source_currency=source_currency, target_currency=target_currency)

    @classmethod
    def _convert_from_usd(cls, day, source_currency, target_currency):
        daily_price = day["price"]
        cache_key = f"{source_currency}_{target_currency}_rate"
        rate = cache.get(cache_key)

        if not rate:
            rate = OpenExchangeClient().latest_rate(target_currency.upper())

            cache.set(cache_key, rate, timeout=1800)

        daily_price = daily_price * Decimal("{:.2f}".format(rate))
        day["price"] = daily_price


    @classmethod
    def _convert_to_usd(cls, day, source_currency, target_currency):
        daily_price = day["price"]
        cache_key = f"{source_currency}_{target_currency}_rate"
        rate = cache.get(cache_key)

        if not rate:
            rate = OpenExchangeClient().latest_rate(source_currency.upper())

            cache.set(cache_key, rate, timeout=1800)

        daily_price = daily_price / Decimal("{:.2f}".format(rate))
        day["price"] = daily_price


    @classmethod
    def _convert_from_any_to_any(cls, day, source_currency, target_currency):
        daily_price = day["price"]
        source_cache_key = f"USD_{source_currency.upper()}_rate"
        target_cache_key = f"USD_{target_currency.upper()}_rate"

        source_usd_rate = cache.get(source_cache_key)

        if not source_usd_rate:
            source_usd_rate = OpenExchangeClient().latest_rate(
                source_currency.upper()
            )
            cache.set(source_cache_key, source_usd_rate, timeout=1800)

        target_usd_rate = cache.get(target_cache_key)

        if not target_usd_rate:
            target_usd_rate = OpenExchangeClient().latest_rate(
                target_currency.upper()
            )

            cache.set(target_cache_key, target_usd_rate, timeout=1800)

        price_in_usd = daily_price / Decimal("{:.2f}".format(source_usd_rate))
        day["price"] = Decimal(
            "{:.2f}".format(
                price_in_usd * Decimal("{:.2f}".format(target_usd_rate))
            )
        )
