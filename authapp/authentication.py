from .models import OwnerUser, BuyerUser
from django.contrib.auth.hashers import check_password
from django.conf import settings


class OwnerAuthenticationBackend:

    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            owner = OwnerUser.objects.get(email=email)
            if owner.check_password(password):
                return owner
            else:
                return None
        except OwnerUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return OwnerUser.objects.get(pk=user_id)
        except OwnerUser.DoesNotExist:
            return None


class BuyerAuthenticationBackend:
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            buyer = BuyerUser.objects.get(email=email)
            if buyer.check_password(password):
                return buyer
            else:
                return None

        except BuyerUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return BuyerUser.objects.get(pk=user_id)
        except BuyerUser.DoesNotExist:
            return None
