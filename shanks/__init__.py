from .app import App, auto_discover_routes, include_routers
from .cors import CORS, enable_cors
from .db import (
    DatabaseConfig,
    MongoDB,
    Redis,
    setup_mongodb,
    setup_mysql,
    setup_postgres,
    setup_redis,
    setup_sqlite,
)
from .request import Request
from .response import Response
from .swagger import SwaggerUI, enable_swagger, swagger
from .cache import (
    cache,
    auto_cache,
    invalidate_cache,
    smart_cache_invalidation,
    get_cache,
)
from .template import render, render_string, render_html

__version__ = "0.2.6"
__author__ = "Ararya"
__email__ = "araryaarch@gmail.com"


# Lazy import ORM to avoid Django settings requirement
def __getattr__(name):
    if name in [
        "Model",
        "User",
        "authenticate",
        "create_user",
        "slugify",
        "CharField",
        "TextField",
        "IntegerField",
        "FloatField",
        "BooleanField",
        "DateField",
        "DateTimeField",
        "EmailField",
        "URLField",
        "SlugField",
        "JSONField",
        "ForeignKey",
        "ManyToManyField",
        "OneToOneField",
        "CASCADE",
        "SET_NULL",
        "PROTECT",
    ]:
        from . import orm

        return getattr(orm, name)

    # Schema imports
    if name in ["Schema", "model"]:
        from . import schema

        return getattr(schema, name)

    # Config imports
    if name in [
        "Config",
        "env",
        "env_bool",
        "env_list",
        "env_int",
        "get_base_dir",
        "get_secret_key",
        "get_debug",
        "get_allowed_hosts",
        "get_database",
        "get_installed_apps",
        "get_middleware",
        "get_templates",
        "get_password_validators",
    ]:
        from . import config

        return getattr(config, name)

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    "App",
    "auto_discover_routes",
    "include_routers",
    "Request",
    "Response",
    "CORS",
    "enable_cors",
    "SwaggerUI",
    "enable_swagger",
    "swagger",
    # Cache
    "cache",
    "auto_cache",
    "invalidate_cache",
    "smart_cache_invalidation",
    "get_cache",
    # Template
    "render",
    "render_string",
    "render_html",
    # ORM
    "Model",
    "User",
    "authenticate",
    "create_user",
    "slugify",
    "CharField",
    "TextField",
    "IntegerField",
    "FloatField",
    "BooleanField",
    "DateField",
    "DateTimeField",
    "EmailField",
    "URLField",
    "SlugField",
    "JSONField",
    "ForeignKey",
    "ManyToManyField",
    "OneToOneField",
    "CASCADE",
    "SET_NULL",
    "PROTECT",
    # Database
    "DatabaseConfig",
    "MongoDB",
    "Redis",
    "setup_postgres",
    "setup_mysql",
    "setup_sqlite",
    "setup_mongodb",
    "setup_redis",
    # Schema
    "Schema",
    "model",
    # Config
    "Config",
    "env",
    "env_bool",
    "env_list",
    "env_int",
    "get_base_dir",
    "get_secret_key",
    "get_debug",
    "get_allowed_hosts",
    "get_database",
    "get_installed_apps",
    "get_middleware",
    "get_templates",
    "get_password_validators",
]

# CLI is available via 'shanks' command after installation
