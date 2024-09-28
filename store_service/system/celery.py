import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "system.settings")
app = Celery("store_service")
app.config_from_object("django.conf.settings", namespace="CELERY")
app.conf.task_default_queue = "store_system_queue"
app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True
