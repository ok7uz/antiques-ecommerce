from .base import *  # Import everything from base.py

# Development settings
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']  # Example allowed hosts for development

# Database settings (replace with your development database configuration)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Path to your local SQLite database file
    }
}

# Media files served directly during development (not recommended for production)
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Example email settings for development (you might use a mail server like MailHog)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
