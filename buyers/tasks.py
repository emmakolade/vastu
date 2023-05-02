from celery import shared_task
from .helpers import send_property_notification


@shared_task
def send_property_notifications_task():

    send_property_notification()


# CELERY_BEAT_SCHEDULE = {
#     'send_property_notifications': {
#         'task': 'path.to.send_property_notifications',
#         'schedule': crontab(hour=0, minute=0),
#     },
# }

# celery - A your_app_name worker - l info
# celery - A your_app_name beat - l info
