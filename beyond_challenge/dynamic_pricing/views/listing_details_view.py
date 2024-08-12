from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from dynamic_pricing.models.listing import Listing
from dynamic_pricing.serializers.listing_details_serializer import (
    ListingDetailsSerializer,
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ListingDetailsView(APIView):

    @swagger_auto_schema(
        responses=openapi.Responses(
            {
                status.HTTP_200_OK: openapi.Response(
                    description="Successful request",
                    schema=openapi.Schema(**ListingDetailsSerializer.SCHEMA),
                ),
                status.HTTP_400_BAD_REQUEST: openapi.Response(
                    description="Bad request error",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "message": openapi.Schema(type=openapi.TYPE_STRING)
                        },
                    ),
                ),
            }
        ),
        operation_description="Get a Listing detail",
    )
    def get(self, request, listing_id):

        listing = Listing.objects.get(id=listing_id)

        return Response(
            ListingDetailsSerializer(
                listing, context={"currency": request.query_params.get("currency")}
            ).data,
            status=status.HTTP_200_OK,
        )
