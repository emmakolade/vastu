from django.core.mail import send_mail
from .models import BuyerProfile
from property_owner.models import PropertyListing


def update_notification_preferences(buyer_profile):
    saved_properties = buyer_profile.saved_properties.all()
    preferences = {}

    for props in saved_properties:
        preferences['property_status'] = props.property_status
        preferences['num_of_bedrooms'] = props.num_of_bedrooms
        preferences['num_of_bathrooms'] = props.num_of_bathrooms
        preferences['property_occupancy'] = props.property_occupancy
        preferences['property_price'] = props.property_price
        preferences['square_ft'] = props.square_ft

    buyer_profile.notification_prefrences = preferences
    buyer_profile.save()
    

def send_property_notification():
    buyers = BuyerProfile.objects.all()

    for buyer in buyers:
        preferences = buyer.notification_prefrences
        if preferences:
            matching_props = PropertyListing.objects.filter(
                property_status=preferences.get('property_status'),
                num_of_bedrooms=preferences.get('num_of_bedrooms'),
                num_of_bathrooms=preferences.get('num_of_bathrooms'),
                property_occupancy=preferences.get('property_occupancy'),
                square_ft=preferences.get('square_ft'),
                property_price__lte=preferences.get('property_price')
            )
            if matching_props.exists():
                send_mail(
                    'New properties available',
                    f'there are {matching_props.count()} new properties that match your preferences.',
                    'fromemail@example.com',
                    [buyer.buyer_user.email],
                    fail_silently=False,
                )
