from .app import App
from .cors import CORS, enable_cors
from .db import (DatabaseConfig, MongoDB, Redis, setup_mongodb, setup_mysql,
                 setup_postgres, setup_redis, setup_sqlite)
from .request import Request
from .response import Response
from .swagger import SwaggerUI, enable_swagger

__version__ = "0.1.0"
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
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    "App",
    "Request",
    "Response",
    "CORS",
    "enable_cors",
    "SwaggerUI",
    "enable_swagger",
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
    "DatabaseConfig",
    "MongoDB",
    "Redis",
    "setup_postgres",
    "setup_mysql",
    "setup_sqlite",
    "setup_mongodb",
    "setup_redis",
]

# CLI is available via 'shanks' command after installation
