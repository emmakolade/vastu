from celery import shared_task
from .helpers import send_property_notification


@shared_task
def send_property_notification():

    send_property_notification()
