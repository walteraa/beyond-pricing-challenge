from django.core.exceptions import ValidationError
from django.core.validators import re
from dynamic_pricing.models.market import Market
import pytest


@pytest.mark.django_db
def test_invalid_due_to_label_missing(invalid_market):
    with pytest.raises(
        ValidationError, match=re.escape("{'label': ['This field cannot be blank.']}")
    ):
        invalid_market.save()


@pytest.mark.django_db
def test_valid(valid_market):
    previous_count = Market.objects.count()

    valid_market.save()

    assert Market.objects.count() == previous_count + 1
