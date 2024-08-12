from rest_framework.serializers import SerializerMethodField
from dynamic_pricing.models.listing import Listing
from dynamic_pricing.serializers.listing_serializer import ListingSerializer
from dynamic_pricing.use_cases.build_calendar import BuildCalendar
from drf_yasg import openapi


class ListingDetailsSerializer(ListingSerializer):

    SCHEMA = {
        "type": openapi.TYPE_OBJECT,
        "properties": {
            "id": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            "title": openapi.Schema(type=openapi.TYPE_STRING),
            "market": openapi.Schema(type=openapi.TYPE_STRING),
            "base_price": openapi.Schema(type=openapi.TYPE_NUMBER),
            "currency": openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=[currency[0] for currency in Listing.Currency.choices()],
            ),
            "host_name": openapi.Schema(type=openapi.TYPE_STRING),
            "calendar": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "date": openapi.Schema(
                            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
                        ),
                        "price": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "currency": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    }

    calendar = SerializerMethodField()

    def get_calendar(self, listing):
        return BuildCalendar.call(listing, self.context.get("currency"))
