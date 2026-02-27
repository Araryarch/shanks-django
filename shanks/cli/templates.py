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


def get_health_view_template(project_name):
    """Health check view template"""
    return f'''"""Health Check Views"""
from shanks import App, render
from dto.base_dto import BaseDTO

router = App()


@router.get("/")
def home(req):
    """Home page"""
    return render(req, "index.html", {{"title": "{project_name}"}})


@router.get("/api/health")
def health(req):
    """Health check endpoint"""
    return BaseDTO.success(
        data={{"service": "{project_name}"}},
        message="Service is healthy"
    )
'''


def get_views_init_template():
    """Views __init__.py template"""
    return '''"""API Views"""

# Import all routers
from .health_view import router as health_router

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

INSTALLED_APPS = get_installed_apps(["internal", "db", "dto"])
MIDDLEWARE = get_middleware()
ROOT_URLCONF = "internal.views"
TEMPLATES = get_templates(BASE_DIR)
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
│   ├── views/            # Views & routes
│   ├── controller/       # Request handlers
│   ├── service/          # Business logic
│   ├── repository/       # Data access
│   └── middleware/       # Custom middleware
├── db/
│   ├── entity/           # Django models
│   ├── migrations/       # Database migrations
│   └── seeds/            # Database seeders
├── dto/                  # Data transfer objects
├── templates/            # HTML templates
└── {project_name}/       # Django config
```

## Template Rendering

Shanks supports Django-style template rendering:

```python
from shanks import render

@router.get('/')
def home(req):
    return render(req, 'index.html', {{'title': 'Welcome'}})
```
"""


def get_index_template(project_name):
    """Index HTML template"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ title }}}} - {project_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 60px 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            text-align: center;
        }}
        h1 {{
            color: #333;
            font-size: 3em;
            margin-bottom: 20px;
        }}
        p {{
            color: #666;
            font-size: 1.2em;
            line-height: 1.6;
            margin-bottom: 30px;
        }}
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }}
        .feature {{
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            transition: transform 0.3s;
        }}
        .feature:hover {{
            transform: translateY(-5px);
        }}
        .feature-icon {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        .feature-title {{
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        .feature-desc {{
            font-size: 0.9em;
            color: #888;
        }}
        .cta {{
            margin-top: 40px;
        }}
        .btn {{
            display: inline-block;
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{{{{ title|default:"{project_name}" }}}}</h1>
        <p>{{{{ message|default:"Welcome to your Shanks Django application!" }}}}</p>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Fast</div>
                <div class="feature-desc">Express.js-like routing</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Simple</div>
                <div class="feature-desc">Clean & intuitive API</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🚀</div>
                <div class="feature-title">Powerful</div>
                <div class="feature-desc">Built on Django</div>
            </div>
        </div>
        
        <div class="cta">
            <a href="/api/health" class="btn">Check API Health</a>
        </div>
    </div>
</body>
</html>
"""
