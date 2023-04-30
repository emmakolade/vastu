from django.urls import path
# from .views import property_listing, property_owner_profile
from .views import create_buyer_profile, edit_buyer_profile, get_buyer_profile

urlpatterns = [
    path("create_profile/", create_buyer_profile, name="create-profile"),
    path("profile/", get_buyer_profile, name="buyer-profile"),
    path("edit_profile/", edit_buyer_profile, name="edit-profile"),

    #     path("create_property", create_property, name="create-property"),
    #     path("list_properties", list_all_properties,
    #          name="list-properties"),
    #     path("update_property/<int:pk>",
    #          update_property, name="update-property"),
    #     path("delete_property<int:pk>",
    #          delete_property, name="deltet-property"),

]
