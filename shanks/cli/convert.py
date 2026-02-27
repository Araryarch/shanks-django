"""Convert Shanks project to pure Django"""

import os
import shutil
import sys
from pathlib import Path

from .banner import print_banner
import re


def _convert_route_file(route_file):
    """Convert a single route file from Shanks to Django views - production ready"""
    content = route_file.read_text(encoding="utf-8")

    # Remove Shanks imports but keep render if present
    has_render = "render" in content
    content = re.sub(r"from shanks import App, render\n", "", content)
    content = re.sub(r"from shanks import App\n", "", content)
    content = re.sub(r"router = App\(\)\n\n", "", content)
    content = re.sub(r"router = App\(\)\n", "", content)

    # Add Django render import if needed
    if has_render:
        content = "from django.shortcuts import render\n" + content

    # Remove all @router decorators
    content = re.sub(
        r'@router\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]\)\n', "", content
    )

    # Remove docstring comments
    content = re.sub(r'"""[^"]*"""', "", content)
    content = re.sub(r"'''[^']*'''", "", content)

    # Rename 'req' parameter to 'request' (Django convention)
    content = re.sub(r"\bdef (\w+)\(req\b", r"def \1(request", content)
    content = re.sub(r"\bdef (\w+)\(req,", r"def \1(request,", content)
    content = re.sub(r"\breq\b", "request", content)

    # Clean up multiple blank lines
    content = re.sub(r"\n\n\n+", "\n\n", content)
    content = content.strip() + "\n"

    route_file.write_text(content, encoding="utf-8")


def _convert_base_dto(base_dto_file):
    """Convert BaseDTO to use Django JsonResponse - production ready"""
    content = base_dto_file.read_text(encoding="utf-8")

    # Remove docstrings
    content = re.sub(r'"""[^"]*"""', "", content)
    content = re.sub(r"'''[^']*'''", "", content)

    # Add Django import at the top
    if "from django.http import JsonResponse" not in content:
        content = "from django.http import JsonResponse\n\n" + content

    # Update success method to return JsonResponse
    content = re.sub(
        r"return response", r"return JsonResponse(response, status=status)", content
    )

    # Clean up multiple blank lines
    content = re.sub(r"\n\n\n+", "\n\n", content)
    content = content.strip() + "\n"

    base_dto_file.write_text(content, encoding="utf-8")


def _convert_controller(controller_file):
    """Convert controller to use Django request API - production ready"""
    content = controller_file.read_text(encoding="utf-8")

    # Remove docstrings
    content = re.sub(r'"""[^"]*"""', "", content)
    content = re.sub(r"'''[^']*'''", "", content)

    # Add Django imports at the top if needed
    if "import json" not in content:
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("from ") or line.startswith("import "):
                lines.insert(i, "import json")
                break
        content = "\n".join(lines)

    # Convert req.query.get() to request.GET.get()
    content = re.sub(r"\breq\.query\.get\(", r"request.GET.get(", content)

    # Convert req.body to JSON parsing
    content = re.sub(
        r"data = req\.body",
        r"data = json.loads(request.body) if request.body else {}",
        content,
    )

    # Convert req.user to request.user
    content = re.sub(r"\breq\.user\b", r"request.user", content)

    # Rename req parameter to request
    content = re.sub(r"\bdef (\w+)\(req\b", r"def \1(request", content)
    content = re.sub(r"\bdef (\w+)\(req,", r"def \1(request,", content)

    # Clean up multiple blank lines
    content = re.sub(r"\n\n\n+", "\n\n", content)
    content = content.strip() + "\n"

    controller_file.write_text(content, encoding="utf-8")


def _convert_settings(settings_file, project_name):
    """Convert settings.py to native Django - production ready"""
    from pathlib import Path
    import secrets

    # Generate a secure secret key
    secret_key = secrets.token_urlsafe(50)

    # Generate production-ready Django settings
    settings_content = f"""from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', '{secret_key}')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'internal',
    'db',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'internal.views'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = '{project_name}.wsgi.application'

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '{project_name}' / 'db.sqlite3',
    }}
}}

AUTH_PASSWORD_VALIDATORS = [
    {{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
"""

    settings_file.write_text(settings_content, encoding="utf-8")


def _convert_wsgi(wsgi_file, project_name):
    """Convert wsgi.py to native Django - production ready"""
    wsgi_content = f"""import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')

application = get_wsgi_application()
"""

    wsgi_file.write_text(wsgi_content, encoding="utf-8")


def _convert_asgi(asgi_file, project_name):
    """Convert asgi.py to native Django - production ready"""
    asgi_content = f"""import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')

application = get_asgi_application()
"""

    asgi_file.write_text(asgi_content, encoding="utf-8")


def _create_env_example(env_file):
    """Create .env.example for production configuration"""
    import secrets

    env_content = f"""SECRET_KEY={secrets.token_urlsafe(50)}
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=sqlite:///db.sqlite3

STATIC_URL=/static/
MEDIA_URL=/media/
"""

    env_file.write_text(env_content, encoding="utf-8")


def _extract_url_patterns(route_file, module_name):
    """Extract URL patterns from route file by parsing Shanks decorators"""
    content = route_file.read_text(encoding="utf-8")
    patterns = []

    lines = content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Look for Shanks decorator pattern: @router.method('/path')
        if line.startswith("@router."):
            # Extract method and path
            match = re.match(
                r'@router\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]\)', line
            )
            if match:
                method = match.group(1)
                path_pattern = match.group(2)

                # Get the function name from next line
                i += 1
                if i < len(lines):
                    func_line = lines[i].strip()
                    if func_line.startswith("def "):
                        func_name = func_line.split("def ")[1].split("(")[0].strip()

                        # Convert Shanks path to Django path
                        # /api/posts/<id> -> api/posts/<int:id>/
                        django_path = path_pattern.lstrip("/")

                        # Don't add trailing slash if path is empty (root path)
                        if django_path and not django_path.endswith("/"):
                            django_path += "/"

                        # Convert <id> to <int:id>
                        django_path = re.sub(r"<(\w+)>", r"<int:\1>", django_path)

                        patterns.append(
                            f"path('{django_path}', {module_name}.{func_name}, name='{func_name}'),"
                        )

        i += 1

    return patterns


def generate_django():
    """Generate pure Django version in separate folder"""
    print_banner()
    print("Generating pure Django version...\n")

    # Check if we're in a Shanks project
    if not Path("manage.py").exists():
        print("[ERROR] Not in a Shanks project directory!")
        print("Run this command from your Shanks project root.")
        sys.exit(1)

    # Get project name from settings
    settings_files = list(Path(".").glob("*/settings.py"))
    if not settings_files:
        print("[ERROR] Could not find Django settings file!")
        sys.exit(1)

    project_name = settings_files[0].parent.name
    django_dir = Path(f"{project_name}-django")

    if django_dir.exists():
        print(f"[ERROR] Directory '{django_dir}' already exists!")
        confirm = input("Delete and recreate? (yes/no): ")
        if confirm.lower() != "yes":
            print("Cancelled.")
            sys.exit(1)
        shutil.rmtree(django_dir)

    print(f"[1/4] Creating Django project structure...")
    django_dir.mkdir()

    # Copy all files except venv and cache
    print(f"[2/4] Copying project files...")
    for item in Path(".").iterdir():
        if item.name in [
            ".venv",
            "venv",
            "__pycache__",
            ".git",
            f"{project_name}-django",
        ]:
            continue

        dest = django_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    print(f"[3/4] Converting Shanks code to Django...")

    # First, extract URL patterns from all view files BEFORE conversion
    views_dir = django_dir / "internal" / "views"
    url_patterns_map = {}

    if views_dir.exists():
        for view_file in views_dir.glob("*_view.py"):
            module_name = view_file.stem  # filename without .py
            url_patterns_map[module_name] = _extract_url_patterns(
                view_file, module_name
            )

    # Convert BaseDTO to use JsonResponse
    base_dto_file = django_dir / "dto" / "base_dto.py"
    if base_dto_file.exists():
        _convert_base_dto(base_dto_file)

    # Convert controllers
    controllers_dir = django_dir / "internal" / "controller"
    if controllers_dir.exists():
        for controller_file in controllers_dir.glob("*_controller.py"):
            _convert_controller(controller_file)

    # Now convert individual view files
    if views_dir.exists():
        for view_file in views_dir.glob("*_view.py"):
            _convert_route_file(view_file)

    # Convert views __init__.py to Django URLs
    views_init = django_dir / "internal" / "views" / "__init__.py"
    if views_init.exists():
        content = views_init.read_text(encoding="utf-8")

        # Add Django imports
        new_content = '''"""Django URL Configuration"""
from django.urls import path, re_path

# Import all view handlers
'''

        # Extract router imports and convert to module imports
        view_modules = []
        lines = content.split("\n")
        for line in lines:
            if "from ." in line and "_view import router" in line:
                # Extract module name
                module = line.split("from .")[1].split(" import")[0]
                view_modules.append(module)
                new_content += f"from . import {module}\n"

        new_content += "\n# Django URL patterns\nurlpatterns = [\n"

        # Add URL patterns from the map we created earlier
        for module in view_modules:
            if module in url_patterns_map:
                for pattern in url_patterns_map[module]:
                    new_content += f"    {pattern}\n"

        new_content += "]\n"

        views_init.write_text(new_content, encoding="utf-8")

    # Convert settings.py to native Django
    settings_file = django_dir / project_name / "settings.py"
    if settings_file.exists():
        _convert_settings(settings_file, project_name)

    # Convert wsgi.py to native Django
    wsgi_file = django_dir / project_name / "wsgi.py"
    if wsgi_file.exists():
        _convert_wsgi(wsgi_file, project_name)

    # Convert asgi.py to native Django (if exists)
    asgi_file = django_dir / project_name / "asgi.py"
    if asgi_file.exists():
        _convert_asgi(asgi_file, project_name)

    # Create .env.example for production
    env_example = django_dir / ".env.example"
    _create_env_example(env_example)

    # Update requirements.txt to remove shanks-django
    requirements = django_dir / "requirements.txt"
    if not requirements.exists():
        requirements.write_text("django>=3.2\n", encoding="utf-8")

    print(f"[4/4] Creating conversion guide...")

    guide = f"""# Django Conversion Complete

Your Shanks project has been converted to production-ready Django.

## Location

{django_dir}/

## What Changed

1. Routes: Converted to Django view functions
2. Controllers: Using Django request API (request.GET, request.POST)
3. BaseDTO: Returns JsonResponse
4. Settings: Native Django with environment variable support
5. WSGI/ASGI: Standard Django configuration

## Production Deployment

1. Copy .env.example to .env and update values:
   ```bash
   cp .env.example .env
   ```

2. Set environment variables:
   - SECRET_KEY: Generate new secret key
   - DEBUG: Set to False in production
   - ALLOWED_HOSTS: Your domain names
   - DATABASE_URL: Your database connection

3. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Deploy with gunicorn or uwsgi:
   ```bash
   gunicorn {project_name}.wsgi:application
   ```

## Security Features

- Environment-based configuration
- Secure secret key generation
- Production security settings (SSL, secure cookies)
- CSRF protection enabled
- XSS protection enabled

## Next Steps

1. Review settings.py for any project-specific configuration
2. Test all endpoints
3. Set up your production database
4. Configure static file serving (nginx/whitenoise)
5. Set up monitoring and logging
"""

    (django_dir / "DEPLOYMENT_GUIDE.md").write_text(guide, encoding="utf-8")

    print(f"\n✓ Django version generated successfully!")
    print(f"\nLocation: {django_dir}/")
    print(f"Guide: {django_dir}/DEPLOYMENT_GUIDE.md")
    print(f"\nProduction-ready features:")
    print(f"  ✓ Environment-based configuration")
    print(f"  ✓ Secure secret key generation")
    print(f"  ✓ Production security settings")
    print(f"  ✓ Clean code without comments")
    print(f"\nNext steps:")
    print(f"  cd {django_dir}")
    print(f"  cp .env.example .env")
    print(f"  python manage.py migrate")
    print(f"  python manage.py runserver")


def kamusari():
    """Convert Shanks project to Django in-place (destructive)"""
    try:
        # Use print instead of print_banner to avoid encoding issues
        print("\n" + "=" * 60)
        print("  SHANKS - KAMUSARI")
        print("  In-place Django Conversion")
        print("=" * 60 + "\n")
    except:
        print("\nKAMUSARI - In-place Django Conversion\n")

    print("WARNING: This will REPLACE all Shanks code with pure Django!")
    print("This operation is DESTRUCTIVE and cannot be undone.")
    print(
        "\nRecommendation: Use 'shanks generate django' instead for a safe conversion.\n"
    )

    confirm1 = input("Are you sure you want to continue? (yes/no): ")
    if confirm1.lower() != "yes":
        print("Cancelled.")
        sys.exit(0)

    confirm2 = input("Type 'KAMUSARI' to confirm: ")
    if confirm2 != "KAMUSARI":
        print("Cancelled.")
        sys.exit(0)

    print("\n[1/4] Backing up project...")
    backup_dir = Path("shanks-backup")
    if backup_dir.exists():
        shutil.rmtree(backup_dir)

    # Get project name from settings
    settings_files = list(Path(".").glob("*/settings.py"))
    if not settings_files:
        print("[ERROR] Could not find Django settings file!")
        sys.exit(1)

    project_name = settings_files[0].parent.name

    # Create backup
    backup_dir.mkdir()
    for item in Path(".").iterdir():
        if item.name in [".venv", "venv", "__pycache__", ".git", "shanks-backup"]:
            continue

        dest = backup_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    print(f"[2/4] Extracting URL patterns...")

    # Extract URL patterns from all route files BEFORE conversion
    routes_dir = Path("internal/routes")
    url_patterns_map = {}

    if routes_dir.exists():
        for route_file in routes_dir.glob("*_route.py"):
            module_name = route_file.stem
            url_patterns_map[module_name] = _extract_url_patterns(
                route_file, module_name
            )

    print(f"[3/4] Converting to Django...")

    # Convert BaseDTO
    base_dto_file = Path("dto/base_dto.py")
    if base_dto_file.exists():
        _convert_base_dto(base_dto_file)

    # Convert controllers
    controllers_dir = Path("internal/controller")
    if controllers_dir.exists():
        for controller_file in controllers_dir.glob("*_controller.py"):
            _convert_controller(controller_file)

    # Convert individual route files
    if routes_dir.exists():
        for route_file in routes_dir.glob("*_route.py"):
            _convert_route_file(route_file)

    # Convert routes __init__.py
    routes_init = Path("internal/routes/__init__.py")
    if routes_init.exists():
        content = routes_init.read_text(encoding="utf-8")

        new_content = '''"""Django URL Configuration"""
from django.urls import path, re_path

# Import all route handlers
'''

        # Extract route modules
        route_modules = []
        lines = content.split("\n")
        for line in lines:
            if "from ." in line and "_route import router" in line:
                module = line.split("from .")[1].split(" import")[0]
                route_modules.append(module)
                new_content += f"from . import {module}\n"

        new_content += "\n# Django URL patterns\nurlpatterns = [\n"

        # Add URL patterns from the map
        for module in route_modules:
            if module in url_patterns_map:
                for pattern in url_patterns_map[module]:
                    new_content += f"    {pattern}\n"

        new_content += "]\n"

        routes_init.write_text(new_content, encoding="utf-8")

    # Convert settings.py to native Django
    settings_file = Path(f"{project_name}/settings.py")
    if settings_file.exists():
        _convert_settings(settings_file, project_name)

    # Convert wsgi.py to native Django
    wsgi_file = Path(f"{project_name}/wsgi.py")
    if wsgi_file.exists():
        _convert_wsgi(wsgi_file, project_name)

    # Convert asgi.py to native Django (if exists)
    asgi_file = Path(f"{project_name}/asgi.py")
    if asgi_file.exists():
        _convert_asgi(asgi_file, project_name)

    # Update requirements
    requirements = Path("requirements.txt")
    if requirements.exists():
        content = requirements.read_text(encoding="utf-8")
        content = content.replace("shanks-django", "# shanks-django (removed)")
        requirements.write_text(content, encoding="utf-8")
    else:
        # Create requirements.txt if it doesn't exist
        Path("requirements.txt").write_text("django>=3.2\n", encoding="utf-8")

    print(f"[4/4] Creating conversion notes...")

    notes = """# KAMUSARI Conversion Complete

Your project has been converted to pure Django IN-PLACE.

## Backup

A backup of your original Shanks project is in: shanks-backup/

## What Changed

1. ✓ Route files converted to Django views (removed @router decorators)
2. ✓ URL patterns automatically generated in internal/routes/__init__.py
3. ✓ 'req' parameters renamed to 'request' (Django convention)
4. ✓ shanks-django removed from requirements

## Files Modified

- internal/routes/__init__.py - Now contains Django urlpatterns
- internal/routes/*_route.py - Converted to plain Django view functions
- requirements.txt - shanks-django dependency removed

## Next Steps

1. Review internal/routes/__init__.py to verify URL patterns
2. Test your application: python manage.py runserver
3. Update any custom middleware or settings if needed

## Restore Backup

If you need to restore your Shanks project:
  
  Windows:
    Remove-Item -Recurse -Force internal, db, dto, config, utils
    Copy-Item -Recurse shanks-backup/* .
  
  Linux/Mac:
    rm -rf internal/ db/ dto/ config/ utils/
    cp -r shanks-backup/* .

## Django Resources

- URL dispatcher: https://docs.djangoproject.com/en/stable/topics/http/urls/
- Views: https://docs.djangoproject.com/en/stable/topics/http/views/
- Request/Response: https://docs.djangoproject.com/en/stable/ref/request-response/
"""

    Path("KAMUSARI_NOTES.md").write_text(notes, encoding="utf-8")

    print(f"\n✓ Conversion complete!")
    print(f"\nBackup: shanks-backup/")
    print(f"Notes: KAMUSARI_NOTES.md")
    print(f"\nYour project is now pure Django!")
    print(f"Test it: python manage.py runserver")
