"""
SORM - Shanks ORM
Clean imports for Shanks ORM functionality
"""

from shanks import Model, CharField, TextField, IntegerField, FloatField
from shanks import BooleanField, DateField, DateTimeField, EmailField
from shanks import URLField, SlugField, JSONField
from shanks import ForeignKey, ManyToManyField, OneToOneField
from shanks import CASCADE, SET_NULL, PROTECT
from shanks import User, authenticate
from shanks import model, Schema


# JSON-like model creation
def table(name, schema):
    """
    Create a model with JSON-like syntax

    Example:
        Category = table("Category", {
            "name": "string:100:unique",
            "slug": "slug:unique",
            "description": "text:blank",
            "created_at": "datetime:auto_now_add"
        })
    """
    return model(name, schema)


__all__ = [
    # Base
    "Model",
    "model",
    "Schema",
    "table",
    # Fields
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
    # Relations
    "ForeignKey",
    "ManyToManyField",
    "OneToOneField",
    # Cascade options
    "CASCADE",
    "SET_NULL",
    "PROTECT",
    # Auth
    "User",
    "authenticate",
]
