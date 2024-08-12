from rest_framework.serializers import SerializerMethodField
from dynamic_pricing.serializers.listing_serializer import ListingSerializer
from dynamic_pricing.use_cases.build_calendar import BuildCalendar


class ListingDetailsSerializer(ListingSerializer):
    calendar = SerializerMethodField()

    def get_calendar(self, listing):
        return BuildCalendar.call(listing, self.context.get("currency"))
