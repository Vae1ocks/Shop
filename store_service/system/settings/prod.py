import os
from .base import *

# True т.к этот файл настроек для сервака, а фронт будет заниматься разработкой,
# когда наш бэк будет находиться на серваке и ему необходима отладка

DEBUG = True

# Для DEBUG = False
# ADMINS = [
#     ('Vaelocks', 'email@email.com'),
#     ('Ophely', 'ophely1992@gmail.com'),
# ]

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db_store',
        'PORT': '5432',
    },
}

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"