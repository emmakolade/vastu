from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PropertyOwnerProfile, PropertyListing
from .serializers import PropertyLisitingSerializer, PropertyOwnerProfileSerializer


@api_view(['GET', 'PUT'])
def property_owner_profile(request):
    try:
        profile = PropertyOwnerProfile.objects.get(owner=request.user)
    except PropertyOwnerProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PropertyOwnerProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PropertyOwnerProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def property_listing(request):
    if request.method == 'GET':
        listings = PropertyListing.objects.filter(
            property_owner__owner_user=request.user)
        serializer = PropertyLisitingSerializer(listings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PropertyLisitingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(property_owner=request.user.propertyownerprofile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
