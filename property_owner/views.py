
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from .models import PropertyOwnerProfile, PropertyListing
from .serializers import PropertyLisitingSerializer, PropertyOwnerProfileSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


# Owner Profile
@swagger_auto_schema(method='GET',)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_owner_profile(request):
    try:
        profile = request.user.profile

    except PropertyOwnerProfile.DoesNotExist:
        return Response({'detail': 'profile not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PropertyOwnerProfileSerializer(profile)
    return Response(serializer.data)


@swagger_auto_schema(method='PUT', request_body=PropertyOwnerProfileSerializer,)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_owner_profile(request):

    try:
        profile = request.user.profile

    except PropertyOwnerProfile.DoesNotExist:
        return Response({'detail': 'profile not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PropertyOwnerProfileSerializer(
        profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='POST', request_body=PropertyOwnerProfileSerializer,)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_owner_profile(request):
    try:
        profile = PropertyOwnerProfile.objects.get(owner_user=request.user)
        serializer = PropertyOwnerProfileSerializer(profile, data=request.data)
    except PropertyOwnerProfile.DoesNotExist:
        serializer = PropertyOwnerProfileSerializer(data=request.data)
    if serializer.is_valid():
        profile = serializer.save(owner_user=request.user)
        return Response(PropertyOwnerProfileSerializer(profile).data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PROPERTY LISTING

@swagger_auto_schema(method='POST', request_body=PropertyLisitingSerializer,)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_property(request):
    if not request.user.is_property_owner:
        return Response({'error': 'only property owners can create or add properties'}, status=status.HTTP_403_FORBIDDEN)

    owner_profile = PropertyOwnerProfile.objects.get(owner_user=request.user)
    serializer = PropertyLisitingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(property_owner=owner_profile)
        update_property_unit(owner_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='GET',)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_properties(request):
    # retrieve all properties of the current user
    owner_profile = PropertyOwnerProfile.objects.get(owner_user=request.user)
    properties = PropertyListing.objects.filter(property_owner=owner_profile)

    serializer = PropertyLisitingSerializer(properties, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='PUT', request_body=PropertyLisitingSerializer,)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_property(request, pk):
    listing = PropertyListing.objects.get(pk=pk)
    if listing.property_owner.owner_user != request.user:
        return Response({'error': 'you can only update your own properties'}, status=status.HTTP_403_FORBIDDEN)

    # update the property with the new data
    serializer = PropertyLisitingSerializer(
        listing, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_property(request, pk):
    listing = PropertyListing.objects.get(pk=pk)
    if listing.property_owner.owner_user != request.user:
        return Response({'error': 'you can only delete your own properties.'}, status=status.HTTP_403_FORBIDDEN)

    listing.delete()
    update_property_unit(listing.property_owner)
    return Response(status=status.HTTP_204_NO_CONTENT)


def update_property_unit(profile):
    property_count = PropertyListing.objects.filter(
        property_owner=profile).count()
    profile.property_unit = property_count
    profile.save()

# class PropertyOwnerProfileView(generics.UpdateAPIView):
#     serializer_class = PropertyOwnerProfileSerializer
#     permission_classes = (IsAuthenticated,)

#     def get_object(self):
#         return PropertyOwnerProfile.objects.get(owner_user=self.request.user)


# class PropertyListingView(generics.ListCreateAPIView):
#     queryset = PropertyListing.objects.all()
#     serializer_class = PropertyLisitingSerializer
#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         return PropertyListing.objects.filter(property_owner=self.request.user)

#     def perform_create(self, serializer):
#         owner_profile_id = self.request.data.get('property_owner')
#         owner_profile = PropertyOwnerProfile.objects.get(id=owner_profile_id)
#         serializer.save(property_owner=owner_profile)
