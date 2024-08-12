from rest_framework.serializers import Serializer, CharField, DecimalField, UUIDField
from drf_yasg import openapi

from dynamic_pricing.models.listing import Listing


class ListingSerializer(Serializer):

    CREATE_SCHEMA = {
        "type": openapi.TYPE_OBJECT,
        "required": ["title", "market", "base_price", "currency"],
        "properties": {
            "title": openapi.Schema(type=openapi.TYPE_STRING),
            "market": openapi.Schema(type=openapi.TYPE_STRING),
            "base_price": openapi.Schema(type=openapi.TYPE_NUMBER),
            "currency": openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=[currency[0] for currency in Listing.Currency.choices()],
            ),
            "host_name": openapi.Schema(type=openapi.TYPE_STRING),
        },
    }

    GET_SCHEMA = {
        "type": openapi.TYPE_OBJECT,
        "properties": {
            "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            **CREATE_SCHEMA["properties"],
        },
    }

    id = UUIDField(required=False)
    title = CharField(max_length=255)
    market = CharField(max_length=255)
    base_price = DecimalField(max_digits=10, decimal_places=2)
    currency = CharField(max_length=150)
    host_name = CharField(
        max_length=255, required=False, allow_null=True, allow_blank=True
    )
