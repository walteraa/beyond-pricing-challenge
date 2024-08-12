from rest_framework.serializers import BaseSerializer
from drf_yasg import openapi
from dynamic_pricing.use_cases.build_calendar import BuildCalendar


class ListingCalendarSerializer(BaseSerializer):
    SCHEMA = {
        "type": openapi.TYPE_ARRAY,
        "items": openapi.Items(
            type=openapi.TYPE_OBJECT,
            properties={
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
                ),
                "price": openapi.Schema(type=openapi.TYPE_NUMBER),
                "currency": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    }

    def to_representation(self, listing):
        currency = self.context.get("currency")
        start_date = self.context.get("start_date")
        end_date = self.context.get("end_date")

        calendar = BuildCalendar.call(listing, currency)
        if start_date:
            calendar = list(filter(lambda day: day["date"] >= start_date, calendar))

        if end_date:
            calendar = list(filter(lambda day: day["date"] <= end_date, calendar))

        return calendar
