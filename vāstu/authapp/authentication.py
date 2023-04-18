from .models import Owner, Buyer
from django.contrib.auth.hashers import check_password
from django.conf import settings


class OwnerAuthenticationBackend:

    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            owner = Owner.objects.get(email=email)
            if owner.check_password(password):
                return owner
            else:
                return None
        except Owner.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Owner.objects.get(pk=user_id)
        except Owner.DoesNotExist:
            return None


class BuyerAuthenticationBackend:
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            buyer = Buyer.objects.get(email=email)
            if buyer.check_password(password):
                return buyer
            else:
                return None

        except Buyer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Buyer.objects.get(pk=user_id)
        except Buyer.DoesNotExist:
            return None
