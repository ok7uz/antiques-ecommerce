from .base import *


DEBUG = True
ALLOWED_HOSTS = ['*']

# Database settings (replace with your development database configuration)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Path to your local SQLite database file
    }
}
