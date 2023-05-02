from django.db import models
from authapp.models import BuyerUser
from django.conf import settings
from property_owner.models import PropertyListing
from django.core.validators import MinValueValidator, MaxValueValidator

User = settings.AUTH_USER_MODEL


class BuyerProfile(models.Model):
    buyer_user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='buyer_profile', primary_key=True)
    profile_picture = models.ImageField(upload_to="photos/", blank=True)

    bio = models.TextField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    facebook_profile = models.URLField(blank=True)
    twitter_profile = models.URLField(blank=True)
    instagram_profile = models.URLField(blank=True)
    saved_properties = models.ManyToManyField(
        PropertyListing, related_name='saved')
    notification_prefrences = models.JSONField(blank=True, null=True)
    

    class Meta:
        verbose_name_plural = "Buyer Profiles"

    def __str__(self):
        return f"{self.buyer_user.full_name} profile"


class BuyerReview(models.Model):
    buyer_user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING)
    property_listing = models.ForeignKey(
        PropertyListing, on_delete=models.CASCADE, related_name='reviews')
    comments = models.TextField(blank=True, null=True)
    edited_comment = models.BooleanField(default=False)
    ratings = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.property_listing.property_title} - {self.buyer_user.username}"


# class SavedProperty(models.Model):
#     buyer_user = models.ForeignKey(
#         BuyerProfile, on_delete=models.CASCADE, related_name='saved_properties')
#     property_listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE)
