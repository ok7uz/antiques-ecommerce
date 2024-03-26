from .base import *


DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.0.117']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
