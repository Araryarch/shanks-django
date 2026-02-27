"""Code generation templates for Shanks CLI"""


def get_base_dto_template():
    """Base DTO template"""
    return '''"""Base DTO for standardized API responses"""


class BaseDTO:
    """Standard API response structure"""
    
    @staticmethod
    def success(data=None, message="Success", status=200, pagination=None):
        """
        Create a successful response
        
        Args:
            data: Response data (default: None)
            message: Success message (default: "Success")
            status: HTTP status code (default: 200)
            pagination: Pagination info dict (default: None)
        
        Returns:
            dict: Standardized response
        """
        response = {
            "status": status,
            "message": message,
            "data": data if data is not None else []
        }
        
        if pagination:
            response["pagination"] = pagination
        else:
            response["pagination"] = {
                "page": 1,
                "limit": 10,
                "total": 0,
                "pages": 0
            }
        
        return response
    
    @staticmethod
    def error(message="Error", status=400, data=None):
        """
        Create an error response
        
        Args:
            message: Error message (default: "Error")
            status: HTTP status code (default: 400)
            data: Additional error data (default: None)
        
        Returns:
            dict: Standardized error response
        """
        response = {
            "status": status,
            "message": message,
            "data": data if data is not None else []
        }
        
        return response
'''


def get_health_route_template(project_name):
    """Health check route template"""
    return f'''"""Health Check Routes"""
from shanks import App
from dto.base_dto import BaseDTO

router = App()


@router.get("/api/health")
def health(req):
    """Health check endpoint"""
    return BaseDTO.success(
        data={{"service": "{project_name}"}},
        message="Service is healthy"
    )
'''


def get_routes_init_template():
    """Routes __init__.py template"""
    return '''"""API Routes"""

# Import all routers
from .health_route import router as health_router

# Export urlpatterns for Django
urlpatterns = [*health_router]
'''


def get_middleware_template():
    """Middleware template"""
    return '''"""Middleware"""


def logger(req, res, next):
    """Log all requests"""
    print(f"[{req.method}] {req.path}")
    return next()
'''


def get_settings_template(project_name):
    """Django settings template"""
    return f'''"""Django Settings"""

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

INSTALLED_APPS = get_installed_apps(["internal", "entity", "dto"])
MIDDLEWARE = get_middleware()
ROOT_URLCONF = "internal.routes"
TEMPLATES = get_templates()
WSGI_APPLICATION = "{project_name}.wsgi.application"
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
'''


def get_wsgi_template(project_name):
    """WSGI template"""
    return f'''"""WSGI"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{project_name}.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
'''


def get_manage_template(project_name):
    """manage.py template"""
    return f'''#!/usr/bin/env python
"""Django management utility"""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
'''


def get_env_example_template():
    """Environment variables example"""
    return """# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=*

# Database (optional)
# DATABASE_URL=postgresql://user:pass@localhost/dbname
"""


def get_readme_template(project_name):
    """README template"""
    return f"""# {project_name}

Shanks Django project

## Quick Start

```bash
cd {project_name}
cp .env.example .env
sorm db push              # Setup database
shanks run                # Start server
```

## Available Commands

```bash
shanks run                # Start development server
shanks create <name> --crud  # Generate CRUD endpoint
sorm db push              # Apply database changes
sorm db pull              # Pull database schema
```

## Project Structure

```
{project_name}/
├── internal/
│   ├── controller/       # Request handlers
│   ├── service/          # Business logic
│   ├── repository/       # Data access
│   ├── routes/           # API routes
│   └── middleware/       # Custom middleware
├── entity/               # Django models
├── dto/                  # Data transfer objects
└── {project_name}/       # Django config
```
"""
