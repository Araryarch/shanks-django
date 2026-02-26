"""Shanks CLI commands - Clean version"""

import os
import subprocess
import sys
from pathlib import Path


SHANKS_ASCII = r"""
   _____ _                 _        
  / ____| |               | |       
 | (___ | |__   __ _ _ __ | | _____ 
  \___ \| '_ \ / _` | '_ \| |/ / __|
  ____) | | | | (_| | | | |   <\__ \
 |_____/|_| |_|\__,_|_| |_|_|\_\___/
                                    
 Express.js-like framework for Django
"""


def print_banner():
    """Print Shanks banner"""
    print(SHANKS_ASCII)


def create_project():
    """Create a new Shanks Django project"""
    if len(sys.argv) < 3:
        print("Usage: shanks new <project_name>")
        sys.exit(1)

    project_name = sys.argv[2]
    print_banner()
    print(f"Creating new Shanks project: {project_name}\n")

    # Create Django project
    try:
        result = subprocess.run(
            [sys.executable, "-m", "django", "startproject", project_name], 
            check=False,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args)
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print("[INFO] Installing Django...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "django"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        result = subprocess.run(
            [sys.executable, "-m", "django", "startproject", project_name], 
            check=False,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"[ERROR] Failed to create project: {result.stderr}")
            sys.exit(1)

    project_dir = Path(project_name)
    config_dir = project_dir / project_name

    # Create directory structure
    print("[1/5] Creating directory structure...")
    internal_dir = project_dir / "internal"
    internal_dir.mkdir(exist_ok=True)
    (internal_dir / "__init__.py").write_text("", encoding='utf-8')

    for subdir in ["controller", "repository", "service", "middleware", "routes"]:
        dir_path = internal_dir / subdir
        dir_path.mkdir(exist_ok=True)
        (dir_path / "__init__.py").write_text("", encoding='utf-8')

    for dir_name in ["dto", "entity", "config", "utils"]:
        dir_path = project_dir / dir_name
        dir_path.mkdir(exist_ok=True)
        (dir_path / "__init__.py").write_text("", encoding='utf-8')

    # Create routes
    print("[2/5] Creating example routes...")
    routes_content = f'''"""API Routes"""
from shanks import App

app = App()


@app.get("api/health")
def health(req):
    """Health check endpoint"""
    return {{"status": "ok", "service": "{project_name}"}}


# Export urlpatterns for Django
urlpatterns = app.get_urls()
'''
    (internal_dir / "routes" / "__init__.py").write_text(routes_content, encoding='utf-8')

    # Create middleware
    middleware_content = '''"""Middleware"""


def logger(req, res, next):
    """Log all requests"""
    print(f"[{req.method}] {req.path}")
    return next()
'''
    (internal_dir / "middleware" / "logger.py").write_text(middleware_content, encoding='utf-8')

    # Update settings.py
    print("[3/5] Configuring Django settings...")
    settings_content = f'''"""Django Settings"""

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
    (config_dir / "settings.py").write_text(settings_content, encoding='utf-8')

    # Update wsgi.py
    wsgi_content = f'''"""WSGI"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{project_name}.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
'''
    (config_dir / "wsgi.py").write_text(wsgi_content, encoding='utf-8')

    # Delete urls.py
    urls_file = config_dir / "urls.py"
    if urls_file.exists():
        urls_file.unlink()

    # Update manage.py
    print("[4/5] Creating management scripts...")
    manage_content = f'''#!/usr/bin/env python
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
    (project_dir / "manage.py").write_text(manage_content, encoding='utf-8')

    # Create .env.example
    env_example = """# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=*

# Database (optional)
# DATABASE_URL=postgresql://user:pass@localhost/dbname
"""
    (project_dir / ".env.example").write_text(env_example, encoding='utf-8')

    # Create README
    print("[5/5] Creating documentation...")
    readme_content = f"""# {project_name}

Shanks Django project

## Quick Start

```bash
cd {project_name}
cp .env.example .env
sorm db push              # Setup database
shanks run                # Start server
```

Visit: http://127.0.0.1:8000/api/health

## Generate CRUD

```bash
shanks create posts --crud
sorm db push              # Update database
```

## Structure

```
{project_name}/
├── internal/
│   ├── controller/    # HTTP handlers
│   ├── routes/        # Route definitions
│   ├── service/       # Business logic
│   └── middleware/    # Middleware
├── entity/            # Database models
└── dto/               # Data Transfer Objects
```
"""
    (project_dir / "README.md").write_text(readme_content, encoding='utf-8')

    # Success message
    print("\n" + "="*50)
    print("SUCCESS! Project created")
    print("="*50)
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    print(f"  sorm db push              # Setup database")
    print(f"  shanks run                # Start server")
    print(f"\nVisit: http://127.0.0.1:8000/api/health")
    print(f"\nGenerate CRUD:")
    print(f"  shanks create posts --crud")
    print()


def create_crud_endpoint():
    """Create CRUD endpoint"""
    if len(sys.argv) < 3:
        print("Usage: shanks create <endpoint_name> --crud")
        sys.exit(1)

    endpoint_name = sys.argv[2]
    model_name = endpoint_name.capitalize().rstrip("s")
    endpoint_plural = endpoint_name.lower()

    if not Path("manage.py").exists():
        print("[ERROR] Not in a Shanks project directory")
        sys.exit(1)

    print(f"Creating CRUD for: {model_name}\n")

    # Create entity
    print("[1/3] Creating model...")
    entity_dir = Path("entity")
    entity_dir.mkdir(exist_ok=True)
    if not (entity_dir / "__init__.py").exists():
        (entity_dir / "__init__.py").write_text("", encoding='utf-8')

    entity_file = entity_dir / f"{endpoint_name}.py"
    entity_content = f'''"""
{model_name} Model
"""
from django.db import models
from django.contrib.auth.models import User


class {model_name}(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        app_label = "entity"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
'''
    entity_file.write_text(entity_content, encoding='utf-8')

    # Update models.py
    models_file = entity_dir / "models.py"
    if models_file.exists():
        models_content = models_file.read_text(encoding='utf-8')
        import_line = f"from .{endpoint_name} import {model_name}"
        if import_line not in models_content:
            models_content += f"\n{import_line}\n"
            models_file.write_text(models_content, encoding='utf-8')
    else:
        models_file.write_text(f"from .{endpoint_name} import {model_name}\n", encoding='utf-8')

    # Create controller
    print("[2/3] Creating controller...")
    controller_dir = Path("internal/controller")
    controller_file = controller_dir / f"{endpoint_name}.py"
    controller_content = f'''"""
{model_name} Controller
"""
from shanks import Response
from entity.{endpoint_name} import {model_name}


def list_{endpoint_plural}(req):
    """List with pagination"""
    page = int(req.query.get("page", 1))
    limit = int(req.query.get("limit", 10))
    offset = (page - 1) * limit

    total = {model_name}.objects.count()
    items = {model_name}.objects.all()[offset : offset + limit]

    return {{
        "data": [
            {{
                "id": item.id,
                "title": item.title,
                "description": item.description,
            }}
            for item in items
        ],
        "pagination": {{"page": page, "limit": limit, "total": total}},
    }}


def get_by_id(req, id):
    """Get by ID"""
    try:
        item = {model_name}.objects.get(id=id)
        return {{
            "id": item.id,
            "title": item.title,
            "description": item.description,
        }}
    except {model_name}.DoesNotExist:
        return Response().status_code(404).json({{"error": "Not found"}})


def create(req):
    """Create"""
    if not req.user.is_authenticated:
        return Response().status_code(401).json({{"error": "Auth required"}})
    
    data = req.body
    item = {model_name}.objects.create(
        title=data.get("title"),
        description=data.get("description", ""),
        created_by=req.user,
    )
    return Response().status_code(201).json({{"id": item.id}})


def update(req, id):
    """Update"""
    if not req.user.is_authenticated:
        return Response().status_code(401).json({{"error": "Auth required"}})
    
    try:
        item = {model_name}.objects.get(id=id)
        data = req.body
        item.title = data.get("title", item.title)
        item.description = data.get("description", item.description)
        item.save()
        return {{"message": "Updated"}}
    except {model_name}.DoesNotExist:
        return Response().status_code(404).json({{"error": "Not found"}})


def delete(req, id):
    """Delete"""
    if not req.user.is_authenticated:
        return Response().status_code(401).json({{"error": "Auth required"}})
    
    try:
        item = {model_name}.objects.get(id=id)
        item.delete()
        return {{"message": "Deleted"}}
    except {model_name}.DoesNotExist:
        return Response().status_code(404).json({{"error": "Not found"}})
'''
    controller_file.write_text(controller_content, encoding='utf-8')

    # Create routes
    print("[3/3] Creating routes...")
    routes_dir = Path("internal/routes")
    routes_file = routes_dir / f"{endpoint_name}.py"
    routes_content = f'''"""
{model_name} Routes
"""
from shanks import App
from internal.controller import {endpoint_name} as controller

router = App()
routes = router.group('api/{endpoint_plural}')


@routes.get('')
def list_{endpoint_plural}(req):
    return controller.list_{endpoint_plural}(req)


@routes.get('<id>')
def get_{endpoint_name}(req, id):
    return controller.get_by_id(req, id)


@routes.post('')
def create_{endpoint_name}(req):
    return controller.create(req)


@routes.put('<id>')
def update_{endpoint_name}(req, id):
    return controller.update(req, id)


@routes.delete('<id>')
def delete_{endpoint_name}(req, id):
    return controller.delete(req, id)


router.include(routes)
'''
    routes_file.write_text(routes_content, encoding='utf-8')

    print("\n" + "="*50)
    print("SUCCESS! CRUD created")
    print("="*50)
    print(f"\nFiles created:")
    print(f"  - entity/{endpoint_name}.py")
    print(f"  - internal/controller/{endpoint_name}.py")
    print(f"  - internal/routes/{endpoint_name}.py")
    print(f"\nNext steps:")
    print(f"  1. Import in internal/routes/__init__.py:")
    print(f"     from . import {endpoint_name}")
    print(f"     app.include({endpoint_name}.router)")
    print(f"  2. Update database:")
    print(f"     sorm db push")
    print(f"\nEndpoints:")
    print(f"  GET    /api/{endpoint_plural}")
    print(f"  GET    /api/{endpoint_plural}/<id>")
    print(f"  POST   /api/{endpoint_plural}")
    print(f"  PUT    /api/{endpoint_plural}/<id>")
    print(f"  DELETE /api/{endpoint_plural}/<id>")
    print()


def create_auth():
    """Create authentication endpoints"""
    if not Path("manage.py").exists():
        print("[ERROR] Not in a Shanks project directory")
        sys.exit(1)

    # Check for --simple flag
    is_simple = "--simple" in sys.argv

    print(f"Creating {'simple' if is_simple else 'complete'} authentication...\n")

    # Create controller
    print("[1/2] Creating auth controller...")
    controller_dir = Path("internal/controller")
    controller_dir.mkdir(parents=True, exist_ok=True)

    if is_simple:
        # Simple auth without email verification
        controller_content = '''"""
Auth Controller - Simple JWT authentication without SMTP
"""
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from shanks import Response
import jwt
import datetime


def _generate_token(user):
    """Generate JWT token for user"""
    secret = getattr(settings, 'SECRET_KEY', 'your-secret-key')
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, secret, algorithm='HS256')


def _decode_token(token):
    """Decode JWT token"""
    try:
        secret = getattr(settings, 'SECRET_KEY', 'your-secret-key')
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def register(req):
    """
    Simple registration without email verification
    
    Body: {
        "username": "string",
        "password": "string",
        "email": "string" (optional)
    }
    """
    data = req.body
    
    username = data.get("username")
    password = data.get("password")
    email = data.get("email", "")
    
    if not username or not password:
        return Response().status_code(400).json({
            "error": "Username and password required"
        })
    
    # Check if user exists
    if User.objects.filter(username=username).exists():
        return Response().status_code(400).json({
            "error": "Username already exists"
        })
    
    # Create user
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )
    
    # Generate token
    token = _generate_token(user)
    
    return Response().status_code(201).json({
        "message": "User created successfully",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    })


def login_user(req):
    """
    Simple login with JWT
    
    Body: {
        "username": "string",
        "password": "string"
    }
    """
    data = req.body
    
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return Response().status_code(400).json({
            "error": "Username and password required"
        })
    
    # Authenticate
    user = authenticate(req.django, username=username, password=password)
    
    if user is None:
        return Response().status_code(401).json({
            "error": "Invalid credentials"
        })
    
    # Generate JWT token
    token = _generate_token(user)
    
    return Response().status_code(200).json({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    })


def logout_user(req):
    """
    Logout (client should delete token)
    Note: JWT is stateless, so logout is handled client-side
    """
    return Response().status_code(200).json({
        "message": "Logout successful. Please delete your token."
    })


def me(req):
    """
    Get current user info from JWT token
    
    Headers: {
        "Authorization": "Bearer <token>"
    }
    """
    # Get token from Authorization header
    auth_header = req.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return Response().status_code(401).json({
            "error": "Authorization header required (Bearer token)"
        })
    
    token = auth_header.replace('Bearer ', '')
    payload = _decode_token(token)
    
    if not payload:
        return Response().status_code(401).json({
            "error": "Invalid or expired token"
        })
    
    try:
        user = User.objects.get(id=payload['user_id'])
        return Response().status_code(200).json({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser
            }
        })
    except User.DoesNotExist:
        return Response().status_code(401).json({
            "error": "User not found"
        })


def refresh_token(req):
    """
    Refresh JWT token
    
    Headers: {
        "Authorization": "Bearer <token>"
    }
    """
    auth_header = req.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return Response().status_code(401).json({
            "error": "Authorization header required"
        })
    
    token = auth_header.replace('Bearer ', '')
    payload = _decode_token(token)
    
    if not payload:
        return Response().status_code(401).json({
            "error": "Invalid or expired token"
        })
    
    try:
        user = User.objects.get(id=payload['user_id'])
        new_token = _generate_token(user)
        
        return Response().status_code(200).json({
            "message": "Token refreshed",
            "token": new_token
        })
    except User.DoesNotExist:
        return Response().status_code(401).json({
            "error": "User not found"
        })
'''
    else:
        # Complete auth with email verification (requires SMTP)
        controller_content = '''"""
Auth Controller - Complete authentication with email verification
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from shanks import Response
import secrets


# In-memory token storage (use Redis in production)
_verification_tokens = {}
_reset_tokens = {}


def register(req):
    """
    Register with email verification
    
    Body: {
        "username": "string",
        "password": "string",
        "email": "string"
    }
    """
    data = req.body
    
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    
    if not username or not password or not email:
        return Response().status_code(400).json({
            "error": "Username, password, and email required"
        })
    
    if User.objects.filter(username=username).exists():
        return Response().status_code(400).json({
            "error": "Username already exists"
        })
    
    if User.objects.filter(email=email).exists():
        return Response().status_code(400).json({
            "error": "Email already exists"
        })
    
    # Create inactive user
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        is_active=False
    )
    
    # Generate verification token
    token = secrets.token_urlsafe(32)
    _verification_tokens[token] = user.id
    
    # Send verification email
    verification_url = f"{settings.SITE_URL}/api/auth/verify?token={token}"
    send_mail(
        "Verify your email",
        f"Click to verify: {verification_url}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    
    return Response().status_code(201).json({
        "message": "User created. Check email for verification link."
    })


def verify_email(req):
    """Verify email with token"""
    token = req.query.get("token")
    
    if not token or token not in _verification_tokens:
        return Response().status_code(400).json({
            "error": "Invalid or expired token"
        })
    
    user_id = _verification_tokens.pop(token)
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    
    return Response().status_code(200).json({
        "message": "Email verified successfully"
    })


def login_user(req):
    """Login"""
    data = req.body
    
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return Response().status_code(400).json({
            "error": "Username and password required"
        })
    
    user = authenticate(req.django, username=username, password=password)
    
    if user is None:
        return Response().status_code(401).json({
            "error": "Invalid credentials"
        })
    
    if not user.is_active:
        return Response().status_code(401).json({
            "error": "Email not verified"
        })
    
    login(req.django, user)
    
    return Response().status_code(200).json({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    })


def logout_user(req):
    """Logout"""
    if not req.user.is_authenticated:
        return Response().status_code(401).json({
            "error": "Not authenticated"
        })
    
    logout(req.django)
    
    return Response().status_code(200).json({
        "message": "Logout successful"
    })


def me(req):
    """Get current user"""
    if not req.user.is_authenticated:
        return Response().status_code(401).json({
            "error": "Not authenticated"
        })
    
    return Response().status_code(200).json({
        "user": {
            "id": req.user.id,
            "username": req.user.username,
            "email": req.user.email,
            "is_staff": req.user.is_staff,
            "is_superuser": req.user.is_superuser
        }
    })


def forgot_password(req):
    """Request password reset"""
    data = req.body
    email = data.get("email")
    
    if not email:
        return Response().status_code(400).json({
            "error": "Email required"
        })
    
    try:
        user = User.objects.get(email=email)
        token = secrets.token_urlsafe(32)
        _reset_tokens[token] = user.id
        
        reset_url = f"{settings.SITE_URL}/api/auth/reset-password?token={token}"
        send_mail(
            "Reset your password",
            f"Click to reset: {reset_url}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        pass  # Don't reveal if email exists
    
    return Response().status_code(200).json({
        "message": "If email exists, reset link sent"
    })


def reset_password(req):
    """Reset password with token"""
    data = req.body
    token = data.get("token")
    new_password = data.get("password")
    
    if not token or not new_password:
        return Response().status_code(400).json({
            "error": "Token and password required"
        })
    
    if token not in _reset_tokens:
        return Response().status_code(400).json({
            "error": "Invalid or expired token"
        })
    
    user_id = _reset_tokens.pop(token)
    user = User.objects.get(id=user_id)
    user.set_password(new_password)
    user.save()
    
    return Response().status_code(200).json({
        "message": "Password reset successful"
    })
'''

    (controller_dir / "auth.py").write_text(controller_content, encoding='utf-8')

    # Create routes
    print("[2/2] Creating auth routes...")
    routes_dir = Path("internal/routes")
    routes_dir.mkdir(parents=True, exist_ok=True)

    if is_simple:
        routes_content = '''"""
Auth Routes - Simple JWT authentication
"""
from shanks import App
from internal.controller import auth as controller

router = App()
routes = router.group('api/auth')


@routes.post('register')
def register(req):
    """Register new user"""
    return controller.register(req)


@routes.post('login')
def login_user(req):
    """Login user"""
    return controller.login_user(req)


@routes.post('logout')
def logout_user(req):
    """Logout user"""
    return controller.logout_user(req)


@routes.get('me')
def me(req):
    """Get current user"""
    return controller.me(req)


@routes.post('refresh')
def refresh_token(req):
    """Refresh JWT token"""
    return controller.refresh_token(req)


router.include(routes)
'''
    else:
        routes_content = '''"""
Auth Routes - Complete authentication
"""
from shanks import App
from internal.controller import auth as controller

router = App()
routes = router.group('api/auth')


@routes.post('register')
def register(req):
    """Register new user"""
    return controller.register(req)


@routes.get('verify')
def verify_email(req):
    """Verify email"""
    return controller.verify_email(req)


@routes.post('login')
def login_user(req):
    """Login user"""
    return controller.login_user(req)


@routes.post('logout')
def logout_user(req):
    """Logout user"""
    return controller.logout_user(req)


@routes.get('me')
def me(req):
    """Get current user"""
    return controller.me(req)


@routes.post('forgot-password')
def forgot_password(req):
    """Request password reset"""
    return controller.forgot_password(req)


@routes.post('reset-password')
def reset_password(req):
    """Reset password"""
    return controller.reset_password(req)


router.include(routes)
'''

    (routes_dir / "auth.py").write_text(routes_content, encoding='utf-8')

    # Success message
    print("\n" + "="*50)
    print("SUCCESS! Auth created")
    print("="*50)
    print(f"\nFiles created:")
    print(f"  - internal/controller/auth.py")
    print(f"  - internal/routes/auth.py")
    print(f"\nNext steps:")
    print(f"  1. Import in internal/routes/__init__.py:")
    print(f"     from . import auth")
    print(f"     app.include(auth.router)")
    
    if is_simple:
        print(f"\nEndpoints:")
        print(f"  POST /api/auth/register   - Register user (returns JWT)")
        print(f"  POST /api/auth/login      - Login (returns JWT)")
        print(f"  POST /api/auth/logout     - Logout")
        print(f"  GET  /api/auth/me         - Get current user (requires JWT)")
        print(f"  POST /api/auth/refresh    - Refresh JWT token")
        print(f"\nUsage:")
        print(f"  1. Register/Login to get JWT token")
        print(f"  2. Include token in requests:")
        print(f"     Authorization: Bearer <token>")
        print(f"\nNote: Requires PyJWT package")
        print(f"  pip install PyJWT")
    else:
        print(f"\n  2. Configure email in settings.py:")
        print(f"     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'")
        print(f"     EMAIL_HOST = 'smtp.gmail.com'")
        print(f"     EMAIL_PORT = 587")
        print(f"     EMAIL_USE_TLS = True")
        print(f"     EMAIL_HOST_USER = 'your-email@gmail.com'")
        print(f"     EMAIL_HOST_PASSWORD = 'your-app-password'")
        print(f"     DEFAULT_FROM_EMAIL = 'your-email@gmail.com'")
        print(f"     SITE_URL = 'http://localhost:8000'")
        print(f"\nEndpoints:")
        print(f"  POST /api/auth/register        - Register user")
        print(f"  GET  /api/auth/verify          - Verify email")
        print(f"  POST /api/auth/login           - Login")
        print(f"  POST /api/auth/logout          - Logout")
        print(f"  GET  /api/auth/me              - Get current user")
        print(f"  POST /api/auth/forgot-password - Request reset")
        print(f"  POST /api/auth/reset-password  - Reset password")
    print()


def show_help():
    """Show help message"""
    print_banner()
    print("Usage: shanks <command> [options]\n")
    print("Commands:")
    print("  new <name>              Create new project")
    print("  create <name> --crud    Generate CRUD endpoints")
    print("  create auth [--simple]  Generate auth endpoints")
    print("  run                     Start development server")
    print("  help                    Show this help\n")
    print("SORM Commands:")
    print("  Use 'sorm' command for database operations")
    print("  sorm db push            Create and apply migrations")
    print("  sorm db reset           Reset database")
    print("  sorm studio             Open admin panel\n")
    print("Examples:")
    print("  shanks new myapp")
    print("  shanks create posts --crud")
    print("  shanks create auth --simple")
    print("  shanks run")
    print("  sorm db push")
    print()


def run_server():
    """Run development server"""
    if not Path("manage.py").exists():
        print("[ERROR] manage.py not found")
        print("Make sure you're in a Shanks project directory")
        sys.exit(1)

    print("Starting development server...\n")
    
    try:
        subprocess.run([sys.executable, "manage.py", "runserver"])
    except KeyboardInterrupt:
        print("\n\nServer stopped")


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    command = sys.argv[1]

    if command == "new":
        create_project()
    elif command == "create":
        if "--crud" in sys.argv:
            create_crud_endpoint()
        elif "auth" in sys.argv:
            create_auth()
        else:
            print("[ERROR] Unknown create command")
            print("Use: shanks create <endpoint> --crud")
            print("     shanks create auth [--simple]")
            sys.exit(1)
    elif command == "run":
        run_server()
    elif command == "help":
        show_help()
    else:
        print(f"[ERROR] Unknown command: {command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()



# SORM CLI
def sorm_main():
    """SORM CLI entry point"""
    if len(sys.argv) < 2:
        show_sorm_help()
        sys.exit(0)

    command = sys.argv[1]

    if command == "db":
        if len(sys.argv) < 3:
            show_sorm_help()
            sys.exit(1)
        
        subcommand = sys.argv[2]
        if subcommand == "push":
            sorm_db_push()
        elif subcommand == "reset":
            sorm_db_reset()
        else:
            print(f"[ERROR] Unknown db command: {subcommand}")
            show_sorm_help()
            sys.exit(1)
    elif command == "studio":
        sorm_studio()
    else:
        print(f"[ERROR] Unknown command: {command}")
        show_sorm_help()
        sys.exit(1)


def sorm_db_push():
    """Create and apply migrations"""
    if not Path("manage.py").exists():
        print("[ERROR] manage.py not found")
        sys.exit(1)

    print("[1/2] Creating migrations...")
    result = subprocess.run(
        [sys.executable, "manage.py", "makemigrations"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("[ERROR] Failed to create migrations")
        print(result.stderr)
        sys.exit(1)

    if "No changes detected" in result.stdout:
        print("  No changes detected")
    else:
        for line in result.stdout.split("\n"):
            if "Migrations for" in line or "Create model" in line:
                print(f"  {line.strip()}")

    print("[2/2] Applying migrations...")
    result = subprocess.run(
        [sys.executable, "manage.py", "migrate"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        for line in result.stdout.split("\n"):
            if "Applying" in line:
                print(f"  {line.strip()}")
        print("\n" + "="*50)
        print("SUCCESS! Database updated")
        print("="*50 + "\n")
    else:
        print("[ERROR] Failed to apply migrations")
        print(result.stderr)
        sys.exit(1)


def sorm_db_reset():
    """Reset database"""
    if not Path("manage.py").exists():
        print("[ERROR] manage.py not found")
        sys.exit(1)

    print("WARNING: This will delete all data!")
    confirm = input("Type 'yes' to confirm: ")

    if confirm.lower() != "yes":
        print("Cancelled")
        sys.exit(0)

    print("Resetting database...")
    result = subprocess.run([sys.executable, "manage.py", "flush", "--noinput"])

    if result.returncode == 0:
        print("\n" + "="*50)
        print("SUCCESS! Database reset")
        print("="*50 + "\n")
    else:
        print("[ERROR] Failed to reset database")
        sys.exit(1)


def sorm_studio():
    """Open admin panel"""
    if not Path("manage.py").exists():
        print("[ERROR] manage.py not found")
        sys.exit(1)

    print("Creating superuser for admin panel...\n")
    result = subprocess.run([sys.executable, "manage.py", "createsuperuser"])

    if result.returncode == 0:
        print("\n" + "="*50)
        print("SUCCESS! Superuser created")
        print("="*50)
        print("\nStarting server...")
        print("Admin: http://127.0.0.1:8000/admin\n")

        try:
            subprocess.run([sys.executable, "manage.py", "runserver"])
        except KeyboardInterrupt:
            print("\n\nServer stopped")


def show_sorm_help():
    """Show SORM help"""
    print(r"""
   _____ ____  _____  __  __ 
  / ____/ __ \|  __ \|  \/  |
 | (___| |  | | |__) | \  / |
  \___ \ |  | |  _  /| |\/| |
  ____) | |__| | | \ \| |  | |
 |_____/ \____/|_|  \_\_|  |_|
                              
 Shanks ORM - Prisma-like CLI
""")
    print("Usage: sorm <command> [options]\n")
    print("Commands:")
    print("  db push                 Create and apply migrations")
    print("  db reset                Reset database (delete all data)")
    print("  studio                  Create superuser and open admin\n")
    print("Examples:")
    print("  sorm db push")
    print("  sorm db reset")
    print("  sorm studio")
    print()
