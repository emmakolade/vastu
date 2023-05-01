
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import PropertyOwnerProfile, PropertyListing
from .serializers import PropertyLisitingSerializer, PropertyOwnerProfileSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q


# OWNER PROFILE

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
def update_property(request, property_id):
    listing = PropertyListing.objects.get(pk=property_id)
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
def delete_property(request, property_id):
    listing = PropertyListing.objects.get(pk=property_id)
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


@swagger_auto_schema(method='GET',)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def property_list(request):
    queryset = PropertyListing.objects.all()

    # filter properties by various attrs
    property_title = request.query_params.get('property_title', None)
    if property_title:
        queryset = queryset.filter(property_title__icontains=property_title)
    
    property_city = request.query_params.get('property_city', None)
    if property_city:
        queryset = queryset.filter(property_city__iexact=property_city)
    
    property_state = request.query_params.get('property_state', None)
    if property_state:
        queryset = queryset.filter(property_state__iexact=property_state)
        
    property_description = request.query_params.get(
        'property_description', None)
    if property_description:
        queryset = queryset.filter(
            property_description__icontains=property_description)
        
    property_price = request.query_params.get('property_price', None)
    if property_price:
        queryset = queryset.filter(property_price__startswith=property_price)
        
    num_of_bathrooms = request.query_params.get('num_of_bathrooms', None)
    if num_of_bathrooms:
        queryset = queryset.filter(num_of_bathrooms__startswith=num_of_bathrooms)
    
    num_of_bedrooms = request.query_params.get('num_of_bedrooms', None)
    if num_of_bedrooms:
        queryset = queryset.filter(
            num_of_bedrooms__startswith=num_of_bedrooms)
    
    property_status = request.query_params.get('property_status', None)
    if property_status:
        queryset = queryset.filter(property_status__iexact=property_status)

    property_occupancy = request.query_params.get('property_occupancy', None)
    if property_occupancy:
        queryset = queryset.filter(
            property_occupancy__iexact=property_occupancy)
        
    serializer = PropertyLisitingSerializer(queryset, many=True)
    return Response(serializer.data)






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
