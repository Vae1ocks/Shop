from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from celery import current_app

User = get_user_model()


@receiver(post_save, sender=User)
def notify_other_service_user_created(sender, instance, created, **kwargs):
    if created:
        current_app.send_task(
            "send_data_user_create_user",
            kwargs={
                "email": instance.email,
                "first_name": instance.first_name,
                "password": instance.password,
            },
            queue="user_system_queue",
        )
