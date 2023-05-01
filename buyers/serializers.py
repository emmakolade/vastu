from rest_framework import serializers

from .models import BuyerProfile, BuyerReview


class BuyerProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source='buyer_user.full_name')
    email = serializers.CharField(source='buyer_user.email', read_only=True)
    username = serializers.CharField(
        source='buyer_user.username', read_only=True)
    phone_number = serializers.CharField(
        source='buyer_user.phone_number')
    sex = serializers.CharField(source='buyer_user.sex')

    class Meta:
        model = BuyerProfile
        fields = ('buyer_user', 'full_name', 'email', 'username', 'phone_number', 'sex', 'profile_picture',
                  'bio', 'address', 'facebook_profile', 'twitter_profile', 'instagram_profile', 'full_name', 'email', 'username', 'phone_number', 'sex',)
        read_only_fields = ('buyer_user', 'email',
                            'username',)

    def update(self, instance, validated_data):
        buyer_user_data = validated_data.pop('buyer_user', None)
        if buyer_user_data:
            buyer_user = instance.buyer_user
            buyer_user.full_name = buyer_user_data.get(
                'full_name', buyer_user.full_name)
            buyer_user.phone_number = buyer_user_data.get(
                'phone_number', buyer_user.phone_number)
            buyer_user.sex = buyer_user_data.get(
                'sex', buyer_user.sex)
            buyer_user.save()
        return super().update(instance, validated_data)


class BuyerReviewSerializer(serializers.ModelSerializer):
    buyer_user = serializers.CharField(
        source='buyer_user.username', read_only=True)

    class Meta:
        model = BuyerReview
        fields = ('id', 'buyer_user', 'property_listing',
                  'comments', 'edited_comment', 'ratings', 'created_at',)
        read_only_fields = ('id', 'buyer_user', 'property_listing',)
