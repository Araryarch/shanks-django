"""ORM wrapper for Shanks Django - Prisma-like syntax"""

from django.db import models
from django.utils.text import slugify as django_slugify


# Re-export Django models with Shanks naming
class Model(models.Model):
    """Base model class with Prisma-like methods"""

    class Meta:
        abstract = True

    @classmethod
    def find_many(cls, **filters):
        """Find many records (Prisma-like)"""
        return cls.objects.filter(**filters)

    @classmethod
    def find_first(cls, **filters):
        """Find first record (Prisma-like)"""
        return cls.objects.filter(**filters).first()

    @classmethod
    def find_unique(cls, **filters):
        """Find unique record (Prisma-like)"""
        try:
            return cls.objects.get(**filters)
        except cls.DoesNotExist:
            return None

    @classmethod
    def create(cls, **data):
        """Create record (Prisma-like)"""
        return cls.objects.create(**data)

    @classmethod
    def update(cls, where, data):
        """Update records (Prisma-like)"""
        return cls.objects.filter(**where).update(**data)

    @classmethod
    def delete_many(cls, **filters):
        """Delete many records (Prisma-like)"""
        return cls.objects.filter(**filters).delete()

    @classmethod
    def count(cls, **filters):
        """Count records (Prisma-like)"""
        if filters:
            return cls.objects.filter(**filters).count()
        return cls.objects.count()

    def update_self(self, **data):
        """Update current instance"""
        for key, value in data.items():
            setattr(self, key, value)
        self.save()
        return self

    def delete_self(self):
        """Delete current instance"""
        self.delete()


# Field types
CharField = models.CharField
TextField = models.TextField
IntegerField = models.IntegerField
FloatField = models.FloatField
BooleanField = models.BooleanField
DateField = models.DateField
DateTimeField = models.DateTimeField
EmailField = models.EmailField
URLField = models.URLField
SlugField = models.SlugField
JSONField = models.JSONField

# Relationship fields
ForeignKey = models.ForeignKey
ManyToManyField = models.ManyToManyField
OneToOneField = models.OneToOneField

# Field options
CASCADE = models.CASCADE
SET_NULL = models.SET_NULL
PROTECT = models.PROTECT


# User helper class with Prisma-like methods (lazy import)
class UserProxy:
    """User proxy with Prisma-like syntax and Django User access"""

    def __getattr__(self, name):
        """Lazy import Django User and forward attribute access"""
        from django.contrib.auth.models import User as DjangoUser

        return getattr(DjangoUser, name)

    @classmethod
    def find_many(cls, **filters):
        """Find many users"""
        from django.contrib.auth.models import User as DjangoUser

        return DjangoUser.objects.filter(**filters)

    @classmethod
    def find_first(cls, **filters):
        """Find first user"""
        from django.contrib.auth.models import User as DjangoUser

        return DjangoUser.objects.filter(**filters).first()

    @classmethod
    def find_unique(cls, **filters):
        """Find unique user"""
        from django.contrib.auth.models import User as DjangoUser

        try:
            return DjangoUser.objects.get(**filters)
        except DjangoUser.DoesNotExist:
            return None

    @classmethod
    def create(cls, username, email, password, **kwargs):
        """Create user"""
        from django.contrib.auth.models import User as DjangoUser

        return DjangoUser.objects.create_user(
            username=username, email=email, password=password, **kwargs
        )

    @classmethod
    def count(cls, **filters):
        """Count users"""
        from django.contrib.auth.models import User as DjangoUser

        if filters:
            return DjangoUser.objects.filter(**filters).count()
        return DjangoUser.objects.count()


# Export User as the proxy instance
User = UserProxy()


def authenticate(username: str, password: str):
    """Authenticate user"""
    from django.contrib.auth import authenticate as django_authenticate

    return django_authenticate(username=username, password=password)


def create_user(username: str, email: str, password: str, **kwargs):
    """Create new user"""
    from django.contrib.auth.models import User as DjangoUser

    return DjangoUser.objects.create_user(
        username=username, email=email, password=password, **kwargs
    )


# Utility functions
def slugify(text, allow_unicode=False):
    """Convert text to slug (URL-friendly string)"""
    return django_slugify(text, allow_unicode=allow_unicode)
