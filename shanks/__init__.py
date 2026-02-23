from .app import App
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
from .orm import (
    CASCADE,
    PROTECT,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    EmailField,
    FloatField,
    ForeignKey,
    IntegerField,
    JSONField,
    ManyToManyField,
    Model,
    OneToOneField,
    SlugField,
    TextField,
    URLField,
    User,
    authenticate,
    create_user,
    slugify,
)
from .request import Request
from .response import Response
from .swagger import SwaggerUI, enable_swagger

__version__ = "0.1.0"
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
__author__ = "Ararya"
__email__ = "araryaarch@gmail.com"

# CLI is available via 'shanks' command after installation
