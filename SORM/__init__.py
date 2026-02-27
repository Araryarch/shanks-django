"""
SORM - Shanks ORM (Deprecated)

This package is deprecated. Use Django models directly in db/entity/ folder.

For database operations, use the SORM CLI:
  sorm db push   - Apply migrations
  sorm db pull   - Show schema
  sorm db reset  - Reset database
  sorm db seed   - Run seeders
"""

# Keep for backward compatibility
try:
    from shanks import Model, CharField, TextField, IntegerField, FloatField
    from shanks import BooleanField, DateField, DateTimeField, EmailField
    from shanks import URLField, SlugField, JSONField
    from shanks import ForeignKey, ManyToManyField, OneToOneField
    from shanks import CASCADE, SET_NULL, PROTECT
    from shanks import User, authenticate
except ImportError:
    pass

__all__ = []
