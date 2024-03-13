from .base import *  # Import everything from base.py

# Production settings
DEBUG = False
ALLOWED_HOSTS = ['your_production_domain']  # Replace with your production domain

# Database settings (replace with your production database configuration)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Example engine (change if needed)
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your_database_host',
        'PORT': '5432',  # Example port (change if needed)
    }
}

# Static files served by a web server (like Nginx or Apache) in production
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Configure media storage for production (e.g., using Amazon S3)

# Email settings for production (use a reliable mail service)
