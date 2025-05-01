"""
Django settings for the Eco Volunteers project.

This file contains all the configuration settings for the Django project.
It defines database connections, installed apps, middleware, static files,
authentication, and other core settings that control the project's behavior.

For more information on Django settings, see:
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of all available settings and their values, see:
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This sets the base directory for the entire project, using pathlib for cross-platform compatibility
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY SETTINGS
# -----------------

# Secret key: Used for cryptographic signing. Keep this secret in production!
# SECURITY WARNING: Never expose this key in public repositories or production environments
# In production, this should be set using environment variables
SECRET_KEY = 'django-insecure-o&^)m3b10jc1o5x)m25s&%3rqnz!2h(#5nof=v8f^*yw)%s9u$'

# Debug mode: Provides detailed error pages and enables additional dev features
# SECURITY WARNING: Set to False in production to avoid exposing sensitive information
DEBUG = True

# Host/domain names that this Django site can serve
# These are used for security validation and to prevent HTTP Host header attacks
# Set to ['*'] for development, change in production for security
# For local development, use: ['localhost', '127.0.0.1', '[::1]']
# For deployment, add your specific domain names
ALLOWED_HOSTS = ['*']  # Allow all hosts for development, restrict in production

# APPLICATION CONFIGURATION
# -------------------------

# INSTALLED_APPS: List of all Django applications that are activated in this project
# This includes Django's built-in apps and our custom apps
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',       # Administration site
    'django.contrib.auth',        # Authentication framework
    'django.contrib.contenttypes', # Content type system (permissions)
    'django.contrib.sessions',    # Session framework
    'django.contrib.messages',    # Messaging framework
    'django.contrib.staticfiles', # Static file management
    
    # Our custom applications
    'portal',  # Main app for the volunteer portal functionality
]

# MIDDLEWARE: List of middleware components that process requests/responses
# These are executed in order (top to bottom for request, bottom to top for response)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',      # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware', # Session support
    'django.middleware.common.CommonMiddleware',          # Common features
    'django.middleware.csrf.CsrfViewMiddleware',          # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Authentication
    'django.contrib.messages.middleware.MessageMiddleware', # User messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Clickjacking protection
]

# Root URL configuration - defines the entry point for URL routing
ROOT_URLCONF = 'eco_volunteers.urls'

# TEMPLATES: Configuration for the template engines
# This project uses Django's default template engine
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Template engine
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Project-level template directories
        'APP_DIRS': True,  # Look for templates in app directories too
        'OPTIONS': {
            'context_processors': [
                # Functions that add variables to the template context
                'django.template.context_processors.debug',  # Adds debug and sql_queries
                'django.template.context_processors.request',  # Adds request object
                'django.contrib.auth.context_processors.auth',  # Adds user variable
                'django.contrib.messages.context_processors.messages',  # Adds messages
            ],
        },
    },
]

# WSGI (Web Server Gateway Interface) application path
# This is the entry point for WSGI servers like Gunicorn to serve the project
WSGI_APPLICATION = 'eco_volunteers.wsgi.application'

# DATABASE CONFIGURATION
# ---------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Default database connection settings
# SQLite is used for development simplicity - change to a more robust DB in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Database engine
        'NAME': BASE_DIR / 'db.sqlite3',         # Database file path
        # For production, consider using PostgreSQL:
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'eco_volunteers_db',
        # 'USER': 'db_user',
        # 'PASSWORD': 'password',
        # 'HOST': 'localhost',
        # 'PORT': '5432',
    }
}

# AUTHENTICATION AND SECURITY
# ---------------------------
# Password validation rules: defines complexity requirements for user passwords
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        # Checks if password is too similar to username or other user attributes
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Ensures minimum password length (default is 8 characters)
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Checks password against a list of common/frequently used passwords
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Ensures password isn't entirely numeric
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# INTERNATIONALIZATION AND LOCALIZATION
# ------------------------------------
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# Default language code for the application
LANGUAGE_CODE = 'en-us'

# Default time zone for the application
# For a list of valid choices, see: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIME_ZONE = 'UTC'

# Enable Django's internationalization system 
# (translation of strings, date/number formatting)
USE_I18N = True

# Enable timezone-aware datetimes
# When True, Django stores datetimes in UTC and performs conversion to the user's timezone
USE_TZ = True

# STATIC FILES CONFIGURATION
# -------------------------
# Static files include CSS, JavaScript, and images that are part of the site design
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# URL prefix for static files - this is what appears in HTML templates: {% static 'path' %}
STATIC_URL = 'static/'

# Directories where Django looks for additional static files besides each app's static folder
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# MEDIA FILES CONFIGURATION
# -----------------------
# Media files are user-uploaded content (e.g., camp images)

# URL prefix for media files
MEDIA_URL = '/media/'

# Absolute filesystem path to the directory where user-uploaded media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# DATABASE FIELD CONFIGURATION
# --------------------------
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# Type of auto-created primary key field
# BigAutoField uses a 64-bit integer, allowing for more entries than AutoField (32-bit)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTHENTICATION REDIRECTS
# ----------------------
# Defines where users are redirected after login/logout actions

# URL to redirect to after successful login (if no 'next' parameter is provided)
LOGIN_REDIRECT_URL = 'home'

# URL to redirect to after logout
LOGOUT_REDIRECT_URL = 'home'

# URL that handles login (used by the login_required decorator)
LOGIN_URL = 'login'
