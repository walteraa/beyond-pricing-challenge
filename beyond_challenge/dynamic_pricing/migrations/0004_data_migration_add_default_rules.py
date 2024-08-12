# Generated by Django 5.1 on 2024-08-12 17:05

from django.db import migrations
from django.utils.translation import Decimal


def create_rules_and_markets(apps, _):

    Market = apps.get_model("dynamic_pricing", "Market")
    Rule = apps.get_model("dynamic_pricing", "Rule")

    saturday_sunday_markets = [
        Market.objects.create(label="paris"),
        Market.objects.create(label="lisbon"),
    ]

    for market in saturday_sunday_markets:
        Rule.objects.create(
            market=market,
            day_of_week="SATURDAY",
            multiplier=Decimal("1.5"),
        )
        Rule.objects.create(
            market=market,
            day_of_week="SUNDAY",
            multiplier=Decimal("1.5"),
        )

    sf_market = Market.objects.create(label="san-francisco")
    Rule.objects.create(
        market=sf_market,
        day_of_week="WEDNESDAY",
        multiplier=Decimal("0.7"),
    )


class Migration(migrations.Migration):

    dependencies = [
        ("dynamic_pricing", "0003_add_created_at_to_listing"),
    ]

    operations = [
        migrations.RunPython(create_rules_and_markets, migrations.RunPython.noop)
    ]
