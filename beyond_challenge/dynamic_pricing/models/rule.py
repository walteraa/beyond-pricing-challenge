from enum import Enum
from uuid import uuid4
from django.db.models import (
    DO_NOTHING,
    CharField,
    DecimalField,
    ForeignKey,
    IntegerChoices,
    PositiveSmallIntegerField,
    UUIDField,
)

from dynamic_pricing.models.base_model import BaseModel
from dynamic_pricing.models.market import Market


class Rule(BaseModel):
    id = UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)

    multiplier = DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)

    class DaysOfWeek(Enum):
        MONDAY = "Monday"
        TUESDAY = "Tuesday"
        WEDNESDAY = "Wednesday"
        THURSDAY = "Thursday"
        FRIDAY = "Friday"
        SATURDAY = "Saturday"
        SUNDAY = "Sunday"

        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)

    day_of_week = CharField(
        max_length=150, choices=DaysOfWeek.choices(), null=False, blank=False
    )

    market = ForeignKey(Market, on_delete=DO_NOTHING, related_name="rules")
