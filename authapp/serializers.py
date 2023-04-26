from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone


import jwt
from .models import User, OwnerUser, BuyerUser


class OwnerUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=150, min_length=8, write_only=True)
    confirm_password = serializers.CharField(
        max_length=150, min_length=8, write_only=True)

    class Meta:
        model = OwnerUser
        fields = ('id', 'full_name', 'email', 'username',
                  'phone_number', 'sex', 'password', 'otp', 'confirm_password',)
        read_only_fields = ('id', 'otp',)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('password do not match')

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email address already exists')

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError('password do not match')

        user = User.objects.create_user(
            **validated_data, password=password)
        # user.is_property_owner = True
        user.save()
        return user


class BuyerUserSerializer(OwnerUserSerializer):
    class Meta:
        model = BuyerUser
        fields = ('id', 'full_name', 'email', 'username',
                  'phone_number', 'sex', 'password', 'otp', 'confirm_password',)
        read_only_fields = ('id', 'otp',)

    def create(self, validated_data):
        user = super().create(validated_data)
        # user.is_buyer = True
        user.save()
        return user


class OTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField(min_value=000000)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get(
                'request'), email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError(
                        'your account is not activated')
                attrs['user'] = user

            else:
                raise serializers.ValidationError('credentials incorrect')
        else:
            raise serializers.ValidationError(
                'Email and password are required')
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not (User.objects.filter(Q(email=value))).exists():
            raise serializers.ValidationError('email address not found')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=150,
        min_length=8,
        write_only=True,
        error_messages={
            'min_length': 'password must be at least 8 characters long.', }
    )
    confirm_password = serializers.CharField(
        max_length=150,
        min_length=8,
        write_only=True,
        error_messages={
            'min_length': 'password must be at least 8 characters long.', }
    )
    token = serializers.CharField()

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('passowrds do not match')
        token = attrs.get('token')

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            user_id = payload['user_id']
            user = get_object_or_404(
                (User, BuyerUser),
                id=user_id
            )
            if not user.is_active:
                raise serializers.ValidationError('your account is inactive')
            if payload.get('type') != 'reset_password':
                raise serializers.ValidationError('invalid token')
            if payload.get('exp') is not None and timezone.now() > timezone.datetime.fromtimestamp(payload['exp']):
                raise serializers.ValidationError('token has expired')
        except jwt.exceptions.DecodeError:
            raise serializers.ValidationError('invalid token')
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        password = self.validated_data['password']
        user = self.validated_data['user']
        user.set_password(password)
        user.save()
