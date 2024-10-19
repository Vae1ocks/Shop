from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "user_service",
        "USER": "admin",
        "PASSWORD": "admin",
        "HOST": "localhost",
        "POST": "5432",
    },
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    }
}

# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_PROTOCOL = "http"
DEFAULT_HOST = (
    ALLOWED_HOSTS[0] if (ALLOWED_HOSTS and ALLOWED_HOSTS[0] != "*") else "127.0.0.1"
)
DEFAULT_PORT = (
    "8000" if DEFAULT_HOST == "127.0.0.1" or DEFAULT_HOST == "localhost" else ""
)
