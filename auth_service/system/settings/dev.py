from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auth_db',
        'USER': 'ophely',
        'PASSWORD': 'ophely159',
        'HOST': 'localhost',
        'POST': '5432'
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'auth_service',
#         'USER': 'admin',
#         'PASSWORD': 'admin',
#     },
# }

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

