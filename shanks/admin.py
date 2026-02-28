"""
Django Admin Panel integration for Shanks with Unfold theme

Usage:
    from shanks import enable_admin

    # In your urls.py
    urlpatterns = [
        *enable_admin(),  # Adds admin panel at /admin/ with Unfold theme
        *your_routes,
    ]

    # Or with custom path
    urlpatterns = [
        *enable_admin(path='dashboard/'),  # Admin at /dashboard/
        *your_routes,
    ]

    # Unfold theme is automatically applied with red, black, white color scheme
"""

from django.contrib import admin
from django.urls import path as url_path
from django.conf import settings


def _setup_unfold():
    """Setup Unfold admin theme with Shanks color scheme"""
    
    # Add unfold to INSTALLED_APPS if not already there
    if hasattr(settings, 'INSTALLED_APPS'):
        installed_apps = list(settings.INSTALLED_APPS)
        
        # Add unfold before django.contrib.admin
        if 'unfold' not in installed_apps:
            try:
                admin_index = installed_apps.index('django.contrib.admin')
                installed_apps.insert(admin_index, 'unfold')
                settings.INSTALLED_APPS = installed_apps
            except ValueError:
                # django.contrib.admin not found, add unfold at the beginning
                installed_apps.insert(0, 'unfold')
                settings.INSTALLED_APPS = installed_apps
    
    # Configure Unfold with Shanks red/black/white theme
    if not hasattr(settings, 'UNFOLD'):
        settings.UNFOLD = {
            "SITE_TITLE": "Shanks Admin",
            "SITE_HEADER": "Shanks Administration",
            "SITE_URL": "/",
            "SITE_ICON": None,
            "SITE_LOGO": None,
            "SITE_SYMBOL": "speed",
            "SHOW_HISTORY": True,
            "SHOW_VIEW_ON_SITE": True,
            "ENVIRONMENT": None,
            "DASHBOARD_CALLBACK": None,
            "LOGIN": {
                "image": None,
            },
            "STYLES": [],
            "SCRIPTS": [],
            "COLORS": {
                "primary": {
                    "50": "239 68 68",   # Red
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
                "font": {
                    "subtle-light": "255 255 255",  # White
                    "subtle-dark": "255 255 255",
                    "default-light": "255 255 255",
                    "default-dark": "255 255 255",
                    "important-light": "239 68 68",  # Red
                    "important-dark": "239 68 68",
                },
            },
            "EXTENSIONS": {
                "modeltranslation": {
                    "flags": {
                        "en": "🇬🇧",
                        "fr": "🇫🇷",
                        "nl": "🇧🇪",
                    },
                },
            },
            "SIDEBAR": {
                "show_search": True,
                "show_all_applications": True,
                "navigation": None,
            },
            "TABS": [],
        }


def enable_admin(path="admin/"):
    """
    Enable Django admin panel with Unfold theme (red, black, white color scheme)

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
    # Setup Unfold theme
    _setup_unfold()
    
    return [
        url_path(path, admin.site.urls),
    ]


def register_model(model, admin_class=None):
    """
    Register a model with Django admin (Unfold theme)

    Args:
        model: Django model class
        admin_class: Optional custom ModelAdmin class (should inherit from unfold.admin.ModelAdmin)

    Example:
        from shanks import register_model
        from unfold.admin import ModelAdmin
        from db.entity.posts_entity import Posts

        # Simple registration
        register_model(Posts)

        # With custom admin using Unfold
        class PostsAdmin(ModelAdmin):
            list_display = ['id', 'title', 'created_at']
            search_fields = ['title']

        register_model(Posts, PostsAdmin)
    """
    if admin_class:
        admin.site.register(model, admin_class)
    else:
        # Use default Unfold ModelAdmin if available
        try:
            from unfold.admin import ModelAdmin
            admin.site.register(model, ModelAdmin)
        except ImportError:
            # Fallback to default Django admin
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


def customize_admin(site_header=None, site_title=None, index_title=None):
    """
    Customize Django admin panel appearance (Unfold theme)

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
