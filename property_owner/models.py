from django.db import models
from authapp.models import OwnerUser
from django.conf import settings


class PropertyOwnerProfile(models.Model):
    owner_user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to="photos/", blank=True)
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    property_unit = models.IntegerField(
        verbose_name='number of properties', default=0)
    facebook_profile = models.URLField(blank=True)
    twitter_profile = models.URLField(blank=True)
    instagram_profile = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = "Owner Profiles"

    def __str__(self):
        return f"{self.full_name} profile"


class PropertyListing(models.Model):
    FOR_SALE = "FS"
    FOR_RENT = "FR"
    PROPERTY_STATUS = [
        (FOR_SALE, "For Sale"),
        (FOR_RENT, "For Rent"),
    ]

    OCCUPIED = "OCC"
    VACANT = "VAC"
    PROPERTY_OCUPPANCY = [
        (OCCUPIED, "Occupied"),
        (VACANT, "Vacant"),
    ]
    property_owner = models.ForeignKey(
        PropertyOwnerProfile, on_delete=models.CASCADE)
    property_title = models.CharField(max_length=200)
    property_full_address = models.CharField(max_length=200)
    property_city = models.CharField(max_length=200)
    property_state = models.CharField(max_length=200)
    property_zipcode = models.CharField(max_length=200)
    property_description = models.TextField(blank=True)
    property_price = models.DecimalField(max_digits=30, decimal_places=2)
    num_of_bedrooms = models.IntegerField()
    num_of_bathrooms = models.IntegerField()
    square_ft = models.IntegerField()
    garage = models.BooleanField(default=False)
    property_status = models.CharField(max_length=8, choices=PROPERTY_STATUS)
    property_occupancy = models.CharField(
        max_length=8, choices=PROPERTY_OCUPPANCY)
    photo_1 = models.ImageField(upload_to='photos/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.property_title
