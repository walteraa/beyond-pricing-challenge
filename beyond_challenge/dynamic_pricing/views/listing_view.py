from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from dynamic_pricing.models.listing import Listing
from dynamic_pricing.serializers.listing_serializer import ListingSerializer
from dynamic_pricing.use_cases.create_listing import CreateListing


class ListingView(APIView):

    def get(self, request):
        listings = Listing.objects.all()

        paginator = LimitOffsetPagination()
        paginated_result = paginator.paginate_queryset(listings, request)
        serializer = ListingSerializer(paginated_result, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ListingSerializer(data=request.data)

        if serializer.is_valid():
            listing = CreateListing.call(**serializer.data)

            return Response(
                ListingSerializer(listing).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
