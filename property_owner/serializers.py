from rest_framework import serializers
from .models import PropertyOwnerProfile, PropertyListing
from authapp.models import OwnerUser


class PropertyOwnerProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source='owner_user.full_name')
    email = serializers.CharField(source='owner_user.email', read_only=True)
    username = serializers.CharField(
        source='owner_user.username', read_only=True)
    phone_number = serializers.CharField(
        source='owner_user.phone_number')
    sex = serializers.CharField(source='owner_user.sex')

    class Meta:
        model = PropertyOwnerProfile
        fields = ('owner_user', 'full_name', 'email', 'username', 'phone_number', 'sex', 'profile_picture',
                  'bio', 'address', 'property_unit', 'facebook_profile', 'twitter_profile', 'instagram_profile', 'full_name', 'email', 'username', 'phone_number', 'sex',)
        read_only_fields = ('owner_user', 'email', 'username', 'property_unit',)

    def update(self, instance, validated_data):
        owner_user_data = validated_data.pop('owner_user', None)
        if owner_user_data:
            owner_user = instance.owner_user
            owner_user.full_name = owner_user_data.get(
                'full_name', owner_user.full_name)
            owner_user.phone_number = owner_user_data.get(
                'phone_number', owner_user.phone_number)
            owner_user.sex = owner_user_data.get(
                'sex', owner_user.sex)
            owner_user.save()
        return super().update(instance, validated_data)


class PropertyLisitingSerializer(serializers.ModelSerializer):
    property_owner = serializers.ReadOnlyField(source='property_owner.id')

    class Meta:
        model = PropertyListing
        fields = '__all__'
        read_only_fields = ('id', 'property_owner',)
