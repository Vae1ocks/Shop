from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

from .models import User


@shared_task(name='send_data_user_create_user')
def create_user_task(**kwargs):
    User.objects.create_user(**kwargs)

