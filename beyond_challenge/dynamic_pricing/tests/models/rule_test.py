from django.core.exceptions import ValidationError
from django.core.validators import re
from dynamic_pricing.models.market import Market
from dynamic_pricing.models.rule import Rule
import pytest


@pytest.mark.django_db
def test_invalid(invalid_rule):
    with pytest.raises(
        ValidationError,
        match=re.escape(
            "{'multiplier': ['This field cannot be null.'], "
            "'day_of_week': ['This field cannot be blank.'], "
            "'market': ['This field cannot be null.']}"
        ),
    ):
        invalid_rule.save()


@pytest.mark.django_db
def test_invalid_due_to_day_of_week_not_valid(valid_rule):
    valid_rule.day_of_week = "another"

    with pytest.raises(
        ValidationError,
        match=re.escape(
            "{'day_of_week': [\"Value 'another' is not a valid choice.\"]}"
        ),
    ):
        valid_rule.save()


@pytest.mark.django_db
def test_valid(valid_rule):
    previous_count = Rule.objects.count()

    valid_rule.save()

    assert Rule.objects.count() == previous_count + 1

    market = Market.objects.filter(label="paris-orly").first()

    assert valid_rule in market.rules.all()
