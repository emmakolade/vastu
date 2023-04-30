from django.urls import path
# from .views import property_listing, property_owner_profile
from .views import get_owner_profile, edit_owner_profile, create_owner_profile


urlpatterns = [
    path("owner/ceate_profile", create_owner_profile, name="create-profile"),
    path("owner/profile", get_owner_profile, name="owner-profile"),
    path("owner/edit_profile", edit_owner_profile, name="edit-owner-profile"),
]
