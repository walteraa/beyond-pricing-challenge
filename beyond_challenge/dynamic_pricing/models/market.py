from uuid import uuid4
from django.db.models import CharField, UUIDField

from dynamic_pricing.models.base_model import BaseModel


class Market(BaseModel):
    id = UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)

    label = CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.label
