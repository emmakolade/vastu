from django.urls import path
from .views import property_listing, property_owner_profile

urlpatterns = [
    path('owner-profile/', property_owner_profile, name='owner-profile'),
    path('property-listing/', property_listing, name='property-lisitng'),
]
