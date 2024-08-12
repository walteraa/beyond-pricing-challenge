from rest_framework.serializers import Serializer, CharField, DecimalField, UUIDField


class ListingSerializer(Serializer):
    id = UUIDField(required=False)
    title = CharField(max_length=255)
    market = CharField(max_length=255)
    base_price = DecimalField(max_digits=10, decimal_places=2)
    currency = CharField(max_length=150)
    host_name = CharField(
        max_length=255, required=False, allow_null=True, allow_blank=True
    )
