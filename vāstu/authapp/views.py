from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BuyerUser, OwnerUser
from .serializers import OwnerUserSerializer, BuyerUserSerializer
from .utils import generate_otp, send_otp, send_welcome_email, send_password_reset_email, send_password_reset_confirmation_email


class RegisterOwnerView(generics.CreateAPIView):
    queryset = OwnerUser.objects.none()
    serializer_class = OwnerUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        otp = generate_otp()
        send_otp(user.email, otp)

        user.otp = otp
        user.is_active = False
        user.save()
        user.save()

        response_data = {
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'username': user.username,
            'phone_number': user.phone_number,
            'sex': user.sex,
            'otp': user.otp,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class RegisterBuyerView(RegisterOwnerView):
    serializer_class = BuyerUserSerializer
