from django.urls import path
# from .views import property_listing, property_owner_profile
from .views import get_owner_profile, edit_owner_profile, create_owner_profile, create_property, list_all_properties, update_property, delete_property


urlpatterns = [
    path("owner/create_profile", create_owner_profile, name="create-profile"),
    path("owner/profile", get_owner_profile, name="owner-profile"),
    path("owner/create_property", create_property, name="create-property"),
    path("owner/list_properties", list_all_properties,
         name="list-properties"),
    path("owner/update_property/<int:pk>",
         update_property, name="update-property"),
    path("owner/delete_property<int:pk>",
         delete_property, name="deltet-property"),

]
