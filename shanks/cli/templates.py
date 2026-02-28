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


@router.get("/api/v1/health")
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


def get_home_view_template(project_name):
    """Home view template (optional, for template rendering)"""
    return f'''"""Home View"""
from shanks import App, render

router = App()


@router.get("/")
def home(req):
    """Home page"""
    return render(req, "index.html", {{"title": "{project_name}"}})
'''


def get_views_init_template():
    """Views __init__.py template"""
    return '''"""Template Views"""

# Import all view routers
from .home_view import router as home_router

# Export urlpatterns for Django
urlpatterns = [*home_router]
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
ROOT_URLCONF = "internal.urls"
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
│   ├── routes/           # API routes
│   ├── views/            # Template views (optional)
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
    <title>{{{{ title|default:"{project_name}" }}}} - Shanks Django</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'JetBrains Mono', monospace;
            background: #0a0a0a;
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            width: 100%;
        }}
        .header {{
            margin-bottom: 60px;
            display: flex;
            align-items: center;
            gap: 24px;
        }}
        .header-image {{
            width: 80px;
            height: 80px;
            object-fit: cover;
        }}
        .header-divider {{
            width: 2px;
            height: 80px;
            background: #dc2626;
        }}
        .header-content {{
            flex: 1;
        }}
        .logo {{
            font-size: 64px;
            font-weight: 900;
            letter-spacing: -2px;
            color: #ffffff;
            margin-bottom: 8px;
        }}
        .tagline {{
            font-size: 16px;
            color: #666;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}
        .code-block {{
            background: #000000;
            border: 1px solid #1a1a1a;
            padding: 30px;
            margin: 40px 0;
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            line-height: 1.8;
            overflow-x: auto;
        }}
        .code-block pre {{
            margin: 0;
            padding: 0;
            font-family: inherit;
            font-size: inherit;
            line-height: inherit;
        }}
        .code-block .comment {{ color: #666; }}
        .code-block .keyword {{ color: #dc2626; }}
        .code-block .function {{ color: #ffffff; }}
        .code-block .string {{ color: #999; }}
        .code-block .decorator {{ color: #dc2626; }}
        .features {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1px;
            background: #1a1a1a;
            border: 1px solid #1a1a1a;
            margin: 60px 0;
        }}
        .feature {{
            background: #0a0a0a;
            padding: 30px;
            transition: background 0.3s;
        }}
        .feature:hover {{
            background: #000000;
        }}
        .feature-title {{
            font-size: 14px;
            font-weight: 700;
            color: #dc2626;
            margin-bottom: 8px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        .feature-desc {{
            font-size: 13px;
            color: #666;
            line-height: 1.6;
        }}
        .links {{
            display: flex;
            gap: 20px;
            margin-top: 60px;
        }}
        .btn {{
            padding: 16px 32px;
            text-decoration: none;
            font-weight: 700;
            font-size: 12px;
            letter-spacing: 2px;
            text-transform: uppercase;
            transition: all 0.3s;
            display: inline-block;
            border: 1px solid;
        }}
        .btn-primary {{
            background: #dc2626;
            color: #ffffff;
            border-color: #dc2626;
        }}
        .btn-primary:hover {{
            background: #b91c1c;
            border-color: #b91c1c;
        }}
        .btn-secondary {{
            background: transparent;
            color: #ffffff;
            border-color: #333;
        }}
        .btn-secondary:hover {{
            border-color: #dc2626;
            color: #dc2626;
        }}
        .footer {{
            margin-top: 80px;
            padding-top: 30px;
            border-top: 1px solid #1a1a1a;
            font-size: 11px;
            color: #333;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        @media (max-width: 768px) {{
            .features {{
                grid-template-columns: 1fr;
            }}
            .logo {{
                font-size: 48px;
            }}
            .links {{
                flex-direction: column;
            }}
            .btn {{
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://github.com/user-attachments/assets/70a7c689-f475-41b4-862b-6b9371d127e9" alt="Shanks" class="header-image">
            <div class="header-divider"></div>
            <div class="header-content">
                <div class="logo">{{{{ title|upper|default:"SHANKS" }}}}</div>
                <div class="tagline">Express.js for Django</div>
            </div>
        </div>

        <div class="code-block">
            <pre><span class="keyword">from</span> shanks <span class="keyword">import</span> App

app = <span class="function">App</span>()

<span class="decorator">@app.get</span>(<span class="string">'api/hello'</span>)
<span class="keyword">def</span> <span class="function">hello</span>(req):
    <span class="keyword">return</span> {{<span class="string">'message'</span>: <span class="string">'Hello World'</span>}}

<span class="comment"># urlpatterns auto-generated! ✨</span></pre>
        </div>

        <div class="features">
            <div class="feature">
                <div class="feature-title">Easy Syntax</div>
                <div class="feature-desc">Familiar decorator-based routing inspired by Express.js</div>
            </div>
            <div class="feature">
                <div class="feature-title">Django ORM</div>
                <div class="feature-desc">Modern database queries with find_many(), create(), update()</div>
            </div>
            <div class="feature">
                <div class="feature-title">Django Power</div>
                <div class="feature-desc">Full Django ecosystem with simplified syntax</div>
            </div>
            <div class="feature">
                <div class="feature-title">Auto Swagger</div>
                <div class="feature-desc">Built-in API documentation and testing interface</div>
            </div>
        </div>

        <div class="links">
            <a href="/api/health" class="btn btn-primary">API Health</a>
            <a href="https://github.com/Araryarch/shanks-django" class="btn btn-secondary" target="_blank">GitHub</a>
        </div>

        <div class="footer">
            Shanks Django Framework — Built by Ararya
        </div>
    </div>
</body>
</html>
"""
