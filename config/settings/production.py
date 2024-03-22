from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Example engine (change if needed)
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'decor$2001',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
