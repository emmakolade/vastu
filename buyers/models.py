from django.db import models
from authapp.models import BuyerUser
from django.conf import settings


class BuyerProfile(models.Model):
    buyer_user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer_profile', primary_key=True)
    profile_picture = models.ImageField(upload_to="photos/", blank=True)
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    facebook_profile = models.URLField(blank=True)
    twitter_profile = models.URLField(blank=True)
    instagram_profile = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = "Buyer Profiles"

    def __str__(self):
        return f"{self.buyer_user.full_name} profile"
