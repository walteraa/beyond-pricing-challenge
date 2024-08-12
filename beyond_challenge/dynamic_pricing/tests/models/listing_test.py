from django.core.exceptions import ValidationError
from django.core.validators import re
from dynamic_pricing.models.listing import Listing
from dynamic_pricing.models.market import Market
import pytest


@pytest.mark.django_db
def test_invalid(invalid_listing):
    with pytest.raises(
        ValidationError,
        match=re.escape(
            "{'title': ['This field cannot be blank.'], "
            "'base_price': ['This field cannot be null.'], "
            "'market': ['This field cannot be null.'], "
            "'currency': ['This field cannot be blank.']}"
        ),
    ):
        invalid_listing.save()


@pytest.mark.django_db
def test_valid(valid_listing):
    previous_count = Listing.objects.count()

    valid_listing.save()

    assert Listing.objects.count() == previous_count + 1

    market = Market.objects.filter(label="paris-orly").first()

    assert valid_listing in market.listings.all()


@pytest.mark.django_db
def test_invalid_base_price(valid_listing):
    valid_listing.base_price = 0
    with pytest.raises(
        ValidationError,
        match=re.escape(
            "{'base_price': ['Ensure this value is greater than or equal to 0.01.']}"
        ),
    ):
        valid_listing.save()


@pytest.mark.django_db
def test_invalid_currency(valid_listing):
    valid_listing.currency = "BRL"
    with pytest.raises(
        ValidationError,
        match=re.escape("{'currency': [\"Value 'BRL' is not a valid choice.\"]}"),
    ):
        valid_listing.save()
