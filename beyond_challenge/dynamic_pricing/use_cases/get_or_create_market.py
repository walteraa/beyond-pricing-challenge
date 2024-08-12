from django.utils.encoding import Decimal
from dynamic_pricing.models.market import Market
from dynamic_pricing.models.rule import Rule


class GetOrCreateMarket:

    @staticmethod
    def call(label: str):

        market_obj, created = Market.objects.get_or_create(label=label.lower())

        if created:
            Rule.objects.create(
                market=market_obj,
                day_of_week=Rule.DaysOfWeek.FRIDAY.name,
                multiplier=Decimal("1.25"),
            )

        return market_obj
