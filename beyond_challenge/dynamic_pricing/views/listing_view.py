from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from dynamic_pricing.models.listing import Listing
from dynamic_pricing.serializers.listing_serializer import ListingSerializer
from dynamic_pricing.use_cases.create_listing import CreateListing
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ListingView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                default=10,
            ),
            openapi.Parameter(
                name="offset",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                default=0,
            ),
        ],
        responses=openapi.Responses(
            {
                status.HTTP_201_CREATED: openapi.Response(
                    description="Successful request",
                    schema=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(**ListingSerializer.GET_SCHEMA),
                    ),
                ),
                status.HTTP_400_BAD_REQUEST: openapi.Response(
                    description="Successful request",
                    schema=openapi.Schema(type=openapi.TYPE_OBJECT),
                ),
            }
        ),
        operation_description="List Listing",
    )
    def get(self, request):
        listings = Listing.objects.all()

        paginator = LimitOffsetPagination()
        paginated_result = paginator.paginate_queryset(listings, request)
        serializer = ListingSerializer(paginated_result, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(**ListingSerializer.CREATE_SCHEMA),
        responses=openapi.Responses(
            {
                status.HTTP_201_CREATED: openapi.Response(
                    description="Successful request",
                    schema=openapi.Schema(**ListingSerializer.GET_SCHEMA),
                ),
                status.HTTP_422_UNPROCESSABLE_ENTITY: openapi.Response(
                    description="Bad request error",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={"errors": openapi.Schema(type=openapi.TYPE_OBJECT)},
                    ),
                ),
            }
        ),
        operation_description="Create a Listing",
    )
    def post(self, request):
        serializer = ListingSerializer(data=request.data)

        if serializer.is_valid():
            listing = CreateListing.call(**serializer.data)

            return Response(
                ListingSerializer(listing).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
