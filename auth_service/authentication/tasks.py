from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
import requests


@shared_task(name='send_mail_secret_code')
def send_mail_code_task(user_email, code=None, first_name=None, message=None):
    subject = 'Подтверждение регистрации.'
    if message:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)
    if first_name:
        message = f'{first_name}, для подтверждения регистрации введите код: {code}'
    else:
        message = f'Пользователь, для подтверждения регистрации введите код: {code}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)
