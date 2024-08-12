from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from dynamic_pricing.models.listing import Listing
from dynamic_pricing.serializers.listing_calendar_serializer import (
    ListingCalendarSerializer,
)
from dynamic_pricing.serializers.listing_details_serializer import (
    ListingDetailsSerializer,
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ListingCalendarView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="start_date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                name="end_date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                name="currency",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            ),
        ],
        responses=openapi.Responses(
            {
                status.HTTP_200_OK: openapi.Response(
                    description="Successful request",
                    schema=openapi.Schema(**ListingCalendarSerializer.SCHEMA),
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

        serializer = ListingCalendarSerializer(
            listing,
            context={
                "currency": request.query_params.get("currency"),
                "start_date": request.query_params.get("start_date"),
                "end_date": request.query_params.get("end_date"),
            },
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
