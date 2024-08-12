from dynamic_pricing.models.listing import Listing
from dynamic_pricing.models.rule import Rule


class GetPriceBaseOnRule:

    @staticmethod
    def call(listing: Listing, day_of_week: int):
        base_price = listing.base_price

        day_of_week_value = Rule.DaysOfWeek.choices()[day_of_week][0]

        rule = listing.market.rules.filter(day_of_week=day_of_week_value).first()

        final_price = base_price * rule.multiplier if rule else base_price

        return final_price
