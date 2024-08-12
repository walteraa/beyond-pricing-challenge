from typing import Optional
from django.utils.encoding import Decimal
from dynamic_pricing.models.market import Market
from dynamic_pricing.models.listing import Listing
from dynamic_pricing.use_cases.get_or_create_market import GetOrCreateMarket


class CreateListing:

    @staticmethod
    def call(
        title: str,
        base_price: Decimal,
        market: str,
        currency: str,
        host_name: Optional[str] = None,
    ):

        market_obj = GetOrCreateMarket.call(market)

        return Listing.objects.create(
            title=title,
            base_price=base_price,
            market=market_obj,
            currency=currency.upper(),
            host_name=host_name,
        )
