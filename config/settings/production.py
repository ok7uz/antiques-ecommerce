from .base import *


DEBUG = False
ALLOWED_HOSTS = ['*']

# Database settings (replace with your production database configuration)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Example engine (change if needed)
        'NAME': 'decor',
        'USER': 'admin',
        'PASSWORD': 'decor$2001',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
