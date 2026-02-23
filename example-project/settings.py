"""Shanks Django Settings - Super Simple"""

from shanks import (
    get_base_dir,
    get_secret_key,
    get_debug,
    get_allowed_hosts,
    get_database,
    get_installed_apps,
    get_middleware,
    get_templates,
    get_password_validators,
)

# Paths
BASE_DIR = get_base_dir(__file__)

# Security
SECRET_KEY = get_secret_key()
DEBUG = get_debug()
ALLOWED_HOSTS = get_allowed_hosts()

# Apps
INSTALLED_APPS = get_installed_apps(["app"])

# Middleware
MIDDLEWARE = get_middleware()

# Routing
ROOT_URLCONF = "app.routes"

# Templates
TEMPLATES = get_templates()

# WSGI
WSGI_APPLICATION = "wsgi.application"

# Database
DATABASES = get_database(BASE_DIR)

# Password validation
AUTH_PASSWORD_VALIDATORS = get_password_validators(DEBUG)

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
