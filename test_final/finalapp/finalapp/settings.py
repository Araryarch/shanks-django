"""Django Settings"""

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

BASE_DIR = get_base_dir(__file__)
SECRET_KEY = get_secret_key()
DEBUG = get_debug()
ALLOWED_HOSTS = get_allowed_hosts()

INSTALLED_APPS = get_installed_apps(["internal", "db", "dto"])
MIDDLEWARE = get_middleware()
ROOT_URLCONF = "internal.urls"
TEMPLATES = get_templates(BASE_DIR)
WSGI_APPLICATION = "finalapp.wsgi.application"
DATABASES = get_database(BASE_DIR)
AUTH_PASSWORD_VALIDATORS = get_password_validators(DEBUG)

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
