
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

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_property(request):
#     if not request.user.is_property_owner:
#         return Response({'error': 'only property owners can create or add properties'}, status=status.HTTP_403_FORBIDDEN)

#     owner_profile =


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

