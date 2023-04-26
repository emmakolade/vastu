from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OwnerUser, BuyerUser
from .serializers import OwnerUserSerializer, BuyerUserSerializer, OTPSerializer, LoginSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer
from .utils import generate_otp, send_otp, send_welcome_email, send_password_reset_email, send_password_reset_confirmation_email

from django.shortcuts import get_object_or_404


class RegisterOwnerView(generics.CreateAPIView):
    queryset = OwnerUser.objects.none()
    serializer_class = OwnerUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        
        otp = generate_otp()
        send_otp(user.email, otp)

        user.otp = otp
        user.is_active = False
        
        user.is_property_owner = True
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
    queryset = BuyerUser.objects.none()
    serializer_class = BuyerUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        otp = generate_otp()
        send_otp(user.email, otp)

        user.otp = otp
        user.is_active = False
        user.is_buyer = True
        user.save()


class VerifyOTPView(generics.UpdateAPIView):
    serializer_class = OTPSerializer
    queryset = User.objects.none()

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            return Response({'status': 'failure', 'message': 'User has already been verified.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']

        if otp == user.otp:
            user.is_active = True
            user.save()
            send_welcome_email(user.email)

            return Response({'status': 'success', 'message': 'your account is now verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'failure', 'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = get_object_or_404(
            User,
            email=email,
        )
        send_password_reset_email(user)
        return Response({'status': 'success', 'message': 'Password reset link sent to email'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        serializer.save()
        send_password_reset_confirmation_email(user)
        return Response({'status': 'success', 'message': 'Password reset successfully'}, status=status.HTTP_200_OK)


class DeleteUserAccountView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.delete()
        return Response({'message': 'account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
