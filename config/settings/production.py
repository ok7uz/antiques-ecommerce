from .base import *  # Import everything from base.py

# Production settings
DEBUG = True
ALLOWED_HOSTS = ['*']  # Replace with your production domain

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


# Configure media storage for production (e.g., using Amazon S3)

# Email settings for production (use a reliable mail service)
