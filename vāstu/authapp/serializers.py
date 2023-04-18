from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import jwt
from .models import BuyerUser, OwnerUser


class OwnerUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=150, min_length=8, write_only=True)
    confirm_password = serializers.CharField(
        max_length=150, min_length=8, write_only=True)

    class Meta:
        model = OwnerUser
        fields = ('id', 'email', 'username', 'full_name',
                  'phone_number', 'sex', 'password', 'otp', 'confirm_password',)
        read_only_fields = ('id', 'otp',)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('password do not match')

        if OwnerUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email address already exists')

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError('password do not match')

        owner = OwnerUser.objects.create_user(
            **validated_data, password=password)
        return owner


class BuyerUserSerializer(OwnerUserSerializer):
    class Meta:
        model = BuyerUser
        fields = ('id', 'email', 'username', 'full_name',
                  'phone_number', 'sex', 'password', 'otp', 'confirm_password',)
        read_only_fields = ('id', 'otp',)
