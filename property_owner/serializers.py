from rest_framework import serializers
from .models import PropertyOwnerProfile, PropertyListing


class PropertyOwnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyOwnerProfile
        fields = '__all__'


class PropertyLisitingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyListing
        fields = '__all__'
