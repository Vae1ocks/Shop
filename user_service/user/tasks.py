from django.core.mail import send_mail
from django.db.models.expressions import RawSQL
from django.conf import settings
from celery import shared_task

from django.contrib.auth import get_user_model


@shared_task(name='send_data_user_create_user')
def create_user_task(**kwargs):
    """
    Для создания пользователя при создании его в auth_service.
    Получает пароль в хешированном виде, так что используется
    create() вместе create_user().
    """
    get_user_model().objects.create(**kwargs, is_verified=True)


@shared_task(name='send_mail_code')
def send_mail_task(user_email, message, subject):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email],
              fail_silently=False)


@shared_task(name='user_service.send_notification')
def send_notification(goods_id, goods_title, price, relative_url):
    """
    Из словаря expected_price выберет ту пару ключ-значение, у которых ключ
    является str(goods_id) (в формате json ключи могут быть только строками, поэтому str().
    Далее войдёт в словарь, который соответствует goods_id и возьмёт из вложенного
    словаря значение ключе price
    """
    price_lookup = RawSQL(
        f"CAST(expected_prices->%s->>'price' AS DECIMAL)",
        (str(goods_id),)
    )
    users = get_user_model().objects.annotate(
        expected_price=price_lookup
    ).filter(
        expected_prices__has_key=str(goods_id),
        expected_price__gte=price
    ).only('email', 'expected_prices')

    url = (f'{settings.DEFAULT_PROTOCOL}://{settings.DEFAULT_HOST}'
           f'{settings.DEFAULT_PORT}{relative_url}')

    for user in users:
        email = user.email
        send_mail_task(
            user_email=email,
            subject='Товар, добавленный вами в "Желаемые" доступен по указанной вами цене!',
            message=f'Товар {goods_title} доступен за {price}р. Вы можете купить его,'
                    f'перейдя по ссылке: {url}'
        )
