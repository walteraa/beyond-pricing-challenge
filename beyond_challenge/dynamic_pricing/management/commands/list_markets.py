from django.core.management.base import BaseCommand

from dynamic_pricing.models.market import Market
from dynamic_pricing.models.rule import Rule


class Command(BaseCommand):
    help = "Displays the market and its rules in the system"

    def handle(self, *args, **kwargs):
        for market in Market.objects.all():
            print(market.label)
            for rule in market.rules.all():
                print(f"\t\t{rule.day_of_week}, {rule.multiplier}")
                print()
