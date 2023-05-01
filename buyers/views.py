from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import BuyerProfile, BuyerReview
from .serializers import BuyerProfileSerializer, BuyerReviewSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(method='GET',)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_buyer_profile(request):
    try:
        profile = request.user.buyer_profile

    except BuyerProfile.DoesNotExist:
        return Response({'detail': 'profile not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BuyerProfileSerializer(profile)
    return Response(serializer.data)


@swagger_auto_schema(method='POST', request_body=BuyerProfileSerializer,)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_buyer_profile(request):
    try:
        profile = BuyerProfile.objects.get(buyer_user=request.user)
        serializer = BuyerProfileSerializer(profile, data=request.data)
    except BuyerProfile.DoesNotExist:
        serializer = BuyerProfileSerializer(data=request.data)
    if serializer.is_valid():
        profile = serializer.save(buyer_user=request.user)
        return Response(BuyerProfileSerializer(profile).data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='PUT', request_body=BuyerProfileSerializer,)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_buyer_profile(request):
    try:
        profile = request.user.buyer_profile
    except BuyerProfile.DoesNotExist:
        return Response({'detail': 'profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BuyerProfileSerializer(profile, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def buyer_review(request):
    try:
        review = request.user.buyer_user
    except BuyerReview.DoesNotExist:
        return Response({'detail': 'buyer not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BuyerReviewSerializer(review, data=request.data, partial=True)
    property