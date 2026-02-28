"""Configuration helpers for Shanks Django"""

import os
from pathlib import Path


class Config:
    """Auto-load environment variables and provide helpers"""

    _loaded = False

    @classmethod
    def load(cls):
        """Auto-load .env file"""
        if cls._loaded:
            return

        try:
            from dotenv import load_dotenv

            load_dotenv()
            cls._loaded = True
        except ImportError:
            # dotenv not installed, skip
            pass

    @classmethod
    def get(cls, key, default=None):
        """Get environment variable with auto-load"""
        cls.load()
        return os.getenv(key, default)

    @classmethod
    def get_bool(cls, key, default=False):
        """Get boolean environment variable"""
        cls.load()
        value = os.getenv(key, str(default))
        return value.lower() in ("true", "1", "yes", "on")

    @classmethod
    def get_list(cls, key, default=None, separator=","):
        """Get list from environment variable"""
        cls.load()
        value = os.getenv(key)
        if value is None:
            return default or []
        return [item.strip() for item in value.split(separator)]

    @classmethod
    def get_int(cls, key, default=0):
        """Get integer environment variable"""
        cls.load()
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default


def env(key, default=None):
    """Shorthand for Config.get()"""
    return Config.get(key, default)


def env_bool(key, default=False):
    """Shorthand for Config.get_bool()"""
    return Config.get_bool(key, default)


def env_list(key, default=None, separator=","):
    """Shorthand for Config.get_list()"""
    return Config.get_list(key, default, separator)


def env_int(key, default=0):
    """Shorthand for Config.get_int()"""
    return Config.get_int(key, default)


# Auto-load on import
Config.load()


def get_base_dir(file_path):
    """Get base directory from __file__"""
    return Path(file_path).resolve().parent


def get_secret_key(default="django-insecure-change-this-in-production"):
    """Get SECRET_KEY from environment"""
    return env("SECRET_KEY", default)


def get_debug(default=True):
    """Get DEBUG from environment"""
    return env_bool("DEBUG", default)


def get_allowed_hosts(default="*"):
    """Get ALLOWED_HOSTS from environment"""
    return env_list("ALLOWED_HOSTS", [default])


def get_database(base_dir):
    """Get database configuration"""
    database_url = env("DATABASE_URL")

    if database_url:
        from .db import DatabaseConfig

        return {"default": DatabaseConfig.from_url(database_url)}

    return {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": base_dir / "db.sqlite3",
        }
    }


def get_installed_apps(extra_apps=None):
    """Get default INSTALLED_APPS with Unfold admin theme"""
    apps = [
        "unfold",  # Unfold admin theme - MUST be before django.contrib.admin
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]

    if extra_apps:
        apps.extend(extra_apps)

    return apps


def get_middleware():
    """Get default MIDDLEWARE"""
    return [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]


def get_templates(base_dir=None):
    """Get default TEMPLATES configuration"""
    dirs = []
    if base_dir:
        templates_dir = base_dir.parent / "templates"
        if templates_dir.exists():
            dirs.append(templates_dir)

    return [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": dirs,
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]


def get_password_validators(debug=True):
    """Get password validators (disabled in debug mode)"""
    if debug:
        return []

    return [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]


def get_unfold_config():
    """Get Unfold admin theme configuration with Shanks red/black/white color scheme"""
    return {
        "SITE_TITLE": env("ADMIN_SITE_TITLE", "Shanks Admin"),
        "SITE_HEADER": env("ADMIN_SITE_HEADER", "SHANKS ADMINISTRATION"),
        "SITE_URL": "/",
        "SITE_ICON": None,
        "SITE_LOGO": None,
        "SITE_SYMBOL": "speed",
        "SHOW_HISTORY": True,
        "SHOW_VIEW_ON_SITE": True,
        "COLORS": {
            "primary": {
                "50": "239 68 68",   # Shanks Red
                "100": "239 68 68",
                "200": "239 68 68",
                "300": "239 68 68",
                "400": "239 68 68",
                "500": "239 68 68",
                "600": "220 38 38",  # Darker red
                "700": "185 28 28",
                "800": "153 27 27",
                "900": "127 29 29",
                "950": "127 29 29",
            },
        },
        "SIDEBAR": {
            "show_search": True,
            "show_all_applications": True,
        },
    }
