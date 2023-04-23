from django.urls import path
from .views import RegisterOwnerView, RegisterBuyerView, VerifyOTPView, LoginView, PasswordResetView,PasswordResetConfirmView, DeleteUserAccountView

urlpatterns = [
    path('register/owner', RegisterOwnerView.as_view(), name='register_owner'),
    path('register/buyer',
         RegisterBuyerView.as_view(), name='register_buyer'),
    path('verify-otp/<int:pk>/', VerifyOTPView.as_view(), name='verify_otp'),
    path('user/login/', LoginView.as_view(), name='login'),
    path('user/delete-account/',
         DeleteUserAccountView.as_view(), name='deleteaccount'),
    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view(),
         name='reset_password_confirm'),
]
