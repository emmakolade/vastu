from django.urls import path
# from .views import property_listing, property_owner_profile
from .views import create_buyer_profile, edit_buyer_profile, get_buyer_profile, buyer_review, edit_buyer_review, delete_buyer_review

urlpatterns = [
    path("create_profile/", create_buyer_profile, name="create-profile"),
    path("profile/", get_buyer_profile, name="buyer-profile"),
    path("edit_profile/", edit_buyer_profile, name="edit-profile"),

    path("buyer_review/<int:property_id>/", buyer_review, name="buyer_review"),
    path("edit_buyer_review/<int:review_id>/",
         edit_buyer_review, name="edit-buyer-review"),
    path("delete_buyer_review/<int:review_id>/",
         delete_buyer_review, name="delete-buyer-review"),
]
