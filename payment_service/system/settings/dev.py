from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "payment_service",
        "USER": "admin",
        "PASSWORD": "admin",
        "HOST": "localhost",
        "POST": 5432,
    },
}
