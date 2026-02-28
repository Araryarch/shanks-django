"""
Django Admin Panel integration for Shanks

Usage:
    from shanks import enable_admin

    # In your urls.py
    urlpatterns = [
        *enable_admin(),  # Adds admin panel at /admin/
        *your_routes,
    ]

    # Or with custom path
    urlpatterns = [
        *enable_admin(path='dashboard/'),  # Admin at /dashboard/
        *your_routes,
    ]
"""

from django.contrib import admin
from django.urls import path as url_path


def enable_admin(path="admin/"):
    """
    Enable Django admin panel

    Args:
        path: URL path for admin panel (default: 'admin/')

    Returns:
        List of URL patterns for admin panel

    Example:
        from shanks import enable_admin

        urlpatterns = [
            *enable_admin(),
            *your_routes,
        ]
    """
    return [
        url_path(path, admin.site.urls),
    ]


def register_model(model, admin_class=None):
    """
    Register a model with Django admin

    Args:
        model: Django model class
        admin_class: Optional custom ModelAdmin class

    Example:
        from shanks import register_model
        from db.entity.posts_entity import Posts

        # Simple registration
        register_model(Posts)

        # With custom admin
        class PostsAdmin(admin.ModelAdmin):
            list_display = ['id', 'title', 'created_at']
            search_fields = ['title']

        register_model(Posts, PostsAdmin)
    """
    if admin_class:
        admin.site.register(model, admin_class)
    else:
        admin.site.register(model)


def unregister_model(model):
    """
    Unregister a model from Django admin

    Args:
        model: Django model class

    Example:
        from shanks import unregister_model
        from django.contrib.auth.models import User

        unregister_model(User)  # Remove User from admin
    """
    admin.site.unregister(model)


# Customize admin site
def customize_admin(site_header=None, site_title=None, index_title=None):
    """
    Customize Django admin panel appearance

    Args:
        site_header: Text at top of admin pages
        site_title: Text in browser title bar
        index_title: Text on admin index page

    Example:
        from shanks import customize_admin

        customize_admin(
            site_header='My App Admin',
            site_title='My App',
            index_title='Dashboard'
        )
    """
    if site_header:
        admin.site.site_header = site_header
    if site_title:
        admin.site.site_title = site_title
    if index_title:
        admin.site.index_title = index_title
