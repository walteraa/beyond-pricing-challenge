from enum import Enum
from uuid import uuid4
from django.core.validators import MinValueValidator
from django.db.models import DO_NOTHING, CharField, DecimalField, ForeignKey, UUIDField
from django.db.models.expressions import Decimal

from dynamic_pricing.models.base_model import BaseModel
from dynamic_pricing.models.market import Market


class Listing(BaseModel):
    id = UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    title = CharField(max_length=255, blank=False, null=False)
    base_price = DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    host_name = CharField(max_length=255, null=True, blank=True)
    market = ForeignKey(Market, on_delete=DO_NOTHING, related_name="listings")

    class Currency(Enum):
        USD = "USD"
        EUR = "EUR"
        JPY = "JPY"
        ILS = "ILS"
        AUD = "AUD"

        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)

    currency = CharField(max_length=150, choices=Currency.choices())
