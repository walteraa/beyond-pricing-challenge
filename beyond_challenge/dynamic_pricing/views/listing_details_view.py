from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from dynamic_pricing.models.listing import Listing
from dynamic_pricing.serializers.listing_details_serializer import (
    ListingDetailsSerializer,
)


class ListingDetailsView(APIView):

    def get(self, request, listing_id):

        listing = Listing.objects.get(id=listing_id)

        return Response(
            ListingDetailsSerializer(
                listing, context={"currency": request.query_params.get("currency")}
            ).data,
            status=status.HTTP_200_OK,
        )
