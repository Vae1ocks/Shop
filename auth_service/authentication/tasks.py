from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task


@shared_task()
def send_mail_code_task(user_email, code, first_name=None):
    subject = 'Подтверждение регистрации.'
    if first_name:
        message = f'{first_name}, для подтверждения регистрации введите код: {code}'
    else:
        message = f'Пользователь, для подтверждения регистрации введите код: {code}'
    print(message)
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)





