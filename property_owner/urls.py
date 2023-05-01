from django.urls import path
# from .views import property_listing, property_owner_profile
from .views import get_owner_profile, edit_owner_profile, create_owner_profile, create_property, list_all_properties, update_property, delete_property, property_list


urlpatterns = [
    path("create_profile/", create_owner_profile, name="create-profile"),
    path("profile/", get_owner_profile, name="owner-profile"),
    path("edit_profile/", edit_owner_profile, name="edit-profile"),
    path("create_property/", create_property, name="create-property"),
    path("list_owner_properties/", list_all_properties,
         name="list-properties"),

    path("update_property/<int:property_id>/",
         update_property, name="update-property"),
    path("delete_property<int:property_id>/",
         delete_property, name="delete-property"),

    path("all_properties/",
         property_list, name="all-properties"),



]
