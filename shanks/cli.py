"""Shanks CLI commands"""

import os
import subprocess
import sys
import time
from pathlib import Path


def format_code():
    """Format code with black"""
    try:
        import black
    except ImportError:
        print("Installing black...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "black"])
        import black

    # Get current directory
    cwd = Path.cwd()

    # Format Python files
    print("🎨 Formatting code with black...")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "black",
            ".",
            "--exclude",
            "/(\.venv|venv|env|\.git|__pycache__|\.pytest_cache|\.mypy_cache|build|dist|\.eggs)/",
        ],
        cwd=cwd,
    )

    if result.returncode == 0:
        print("✨ Code formatted successfully!")
    else:
        print("❌ Formatting failed")
        sys.exit(1)


def lint_code():
    """Lint code with flake8"""
    try:
        import flake8
    except ImportError:
        print("Installing flake8...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flake8"])

    print("🔍 Linting code with flake8...")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "flake8",
            ".",
            "--exclude=.venv,venv,env,.git,__pycache__,.pytest_cache,.mypy_cache,build,dist,.eggs",
            "--max-line-length=127",
            "--extend-ignore=E203,W503",
        ]
    )

    if result.returncode == 0:
        print("✅ No linting errors!")
    else:
        print("⚠️  Linting issues found")
        sys.exit(1)


def run_server():
    """Run Django development server with auto-reload (like nodemon)"""
    try:
        import watchdog
    except ImportError:
        print("Installing watchdog for auto-reload...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "watchdog"])

    # Check if manage.py exists
    if not Path("manage.py").exists():
        print("❌ manage.py not found!")
        print("Make sure you're in a Shanks project directory.")
        sys.exit(1)

    # Get host and port from args
    host = "127.0.0.1"
    port = "8000"

    if len(sys.argv) > 2:
        for arg in sys.argv[2:]:
            if ":" in arg:
                host, port = arg.split(":")
            elif arg.isdigit():
                port = arg

    print(f"🚀 Starting Shanks development server...")
    print(f"📡 Server running at http://{host}:{port}")
    print(f"🔄 Auto-reload enabled")
    print(f"⏹️  Press Ctrl+C to stop\n")

    # Run Django development server with suppressed output
    try:
        # Suppress Django startup messages
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"

        process = subprocess.Popen(
            [sys.executable, "manage.py", "runserver", f"{host}:{port}", "--noreload"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        # Filter output to only show relevant info
        for line in process.stdout:
            # Skip Django version and startup messages
            if any(
                skip in line
                for skip in [
                    "Watching for file changes",
                    "Performing system checks",
                    "System check identified",
                    "Django version",
                    "Starting development server",
                    "Quit the server",
                ]
            ):
                continue
            # Show errors and important messages
            if line.strip():
                print(line.rstrip())

        process.wait()
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)


def create_project():
    """Create a new Shanks Django project with Go-like architecture"""
    if len(sys.argv) < 3:
        print("Usage: shanks new <project_name>")
        sys.exit(1)

    project_name = sys.argv[2]
    print(f"🎉 Creating new Shanks project: {project_name}")

    # Create Django project
    try:
        subprocess.run(
            [sys.executable, "-m", "django", "startproject", project_name], check=True
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ Django not found. Installing Django...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "django"])
        subprocess.run(
            [sys.executable, "-m", "django", "startproject", project_name], check=True
        )

    project_dir = Path(project_name)
    config_dir = project_dir / project_name

    # Create Go-like architecture
    internal_dir = project_dir / "internal"
    internal_dir.mkdir(exist_ok=True)
    (internal_dir / "__init__.py").write_text("")

    # Create internal subdirectories
    for subdir in ["controller", "repository", "service", "middleware", "routes"]:
        dir_path = internal_dir / subdir
        dir_path.mkdir(exist_ok=True)
        (dir_path / "__init__.py").write_text("")

    # Create other directories
    for dir_name in ["dto", "entity", "config", "utils"]:
        dir_path = project_dir / dir_name
        dir_path.mkdir(exist_ok=True)
        (dir_path / "__init__.py").write_text("")

    # Create routes with example
    routes_content = '''"""API Routes"""
from shanks import App, swagger

app = App()  # Cache enabled by default!

# Enable Swagger - applies to all endpoints!
app.use(swagger(title="{project_name} API", version="1.0.0"))


@app.get("api/health")
def health(req):
    """Health check"""
    return {{"status": "ok", "service": "{project_name}"}}


# urlpatterns auto-generated! ✨
'''.format(project_name=project_name)
    (internal_dir / "routes" / "__init__.py").write_text(routes_content)

    # Create example middleware
    middleware_content = '''"""Middleware"""


def logger(req, res, next):
    """Log all requests - Express.js style"""
    print(f"[{{req.method}}] {{req.path}}")
    next()
'''
    (internal_dir / "middleware" / "logger.py").write_text(middleware_content)

    # Update settings.py
    settings_content = '''"""Shanks Django Settings"""

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

# Paths
BASE_DIR = get_base_dir(__file__)

# Security
SECRET_KEY = get_secret_key()
DEBUG = get_debug()
ALLOWED_HOSTS = get_allowed_hosts()

# Apps
INSTALLED_APPS = get_installed_apps(["internal", "entity", "dto"])

# Middleware
MIDDLEWARE = get_middleware()

# Routing
ROOT_URLCONF = "internal.routes"

# Templates
TEMPLATES = get_templates()

# WSGI
WSGI_APPLICATION = "{project_name}.wsgi.application"

# Database
DATABASES = get_database(BASE_DIR)

# Password validation
AUTH_PASSWORD_VALIDATORS = get_password_validators(DEBUG)

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
'''.format(project_name=project_name)
    (config_dir / "settings.py").write_text(settings_content)

    # Update wsgi.py
    wsgi_content = '''"""WSGI"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{project_name}.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
'''.format(project_name=project_name)
    (config_dir / "wsgi.py").write_text(wsgi_content)

    # Delete urls.py
    urls_file = config_dir / "urls.py"
    if urls_file.exists():
        urls_file.unlink()

    # Override manage.py to suppress warnings
    manage_content = '''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import warnings


def main():
    """Run administrative tasks."""
    # Suppress sys.prefix warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="site")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
'''.format(project_name=project_name)
    (project_dir / "manage.py").write_text(manage_content)

    # Create .env.example
    env_example = """# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=*

# Database (optional)
# DATABASE_URL=postgresql://user:pass@localhost/dbname
"""
    (project_dir / ".env.example").write_text(env_example)

    # Create README.md
    readme_content = """# {project_name}

Shanks Django project with Go-like architecture

## Structure

```
{project_name}/
├── internal/           # Internal application code
│   ├── controller/    # HTTP handlers
│   ├── repository/    # Data access layer
│   ├── service/       # Business logic
│   ├── middleware/    # Middleware functions
│   └── routes/        # Route definitions
├── entity/            # Database models
├── dto/               # Data Transfer Objects
├── config/            # Configuration files
├── utils/             # Utility functions
└── {project_name}/    # Django settings
```

## Quick Start

```bash
# Install dependencies
pip install shanks-django

# Copy environment file
cp .env.example .env

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Visit: http://127.0.0.1:8000/api/health
Swagger: http://127.0.0.1:8000/docs

## Generate CRUD

```bash
shanks create posts --crud
shanks create auth --simple
```
""".format(project_name=project_name)
    (project_dir / "README.md").write_text(readme_content)

    print(f"\n✅ Project created successfully!")
    print(f"\n📁 Go-like architecture:")
    print(f"  {project_name}/")
    print(f"  ├── internal/")
    print(f"  │   ├── controller/    # HTTP handlers")
    print(f"  │   ├── repository/    # Data access")
    print(f"  │   ├── service/       # Business logic")
    print(f"  │   ├── middleware/    # Middleware")
    print(f"  │   └── routes/        # Routes")
    print(f"  ├── entity/            # Models")
    print(f"  ├── dto/               # DTOs")
    print(f"  ├── config/            # Config")
    print(f"  └── utils/             # Utils")
    print(f"\n🚀 Next steps:")
    print(f"  cd {project_name}")
    print(f"  cp .env.example .env")
    print(f"  python manage.py migrate")
    print(f"  python manage.py runserver")
    print(f"\n🌐 Visit: http://127.0.0.1:8000/api/health")
    print(f"\n📚 Swagger: http://127.0.0.1:8000/docs")


def create_crud_endpoint():
    """Create CRUD endpoint with Go-like architecture"""
    if len(sys.argv) < 3:
        print("Usage: shanks create <endpoint_name> --crud")
        print("Example: shanks create posts --crud")
        sys.exit(1)

    endpoint_name = sys.argv[2]
    model_name = endpoint_name.capitalize().rstrip("s")
    endpoint_plural = endpoint_name.lower()

    if not Path("manage.py").exists():
        print("❌ Not in a Shanks project directory!")
        sys.exit(1)

    # Create entity (model) - use Django models directly
    entity_dir = Path("entity")
    entity_dir.mkdir(exist_ok=True)
    if not (entity_dir / "__init__.py").exists():
        (entity_dir / "__init__.py").write_text("")

    entity_file = entity_dir / f"{endpoint_name}.py"
    entity_content = f'''"""
{model_name} Entity
"""
from django.db import models
from django.contrib.auth.models import User


class {model_name}(models.Model):
    """
{model_name} model
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="{endpoint_plural}")

    class Meta:
        app_label = "entity"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    # Prisma-like methods
    @classmethod
    def find_many(cls, **filters):
        return cls.objects.filter(**filters)

    @classmethod
    def find_unique(cls, **filters):
        try:
            return cls.objects.get(**filters)
        except cls.DoesNotExist:
            return None

    @classmethod
    def count(cls, **filters):
        if filters:
            return cls.objects.filter(**filters).count()
        return cls.objects.count()

    def update_self(self, **data):
        for key, value in data.items():
            setattr(self, key, value)
        self.save()
        return self

    def delete_self(self):
        self.delete()
'''
    entity_file.write_text(entity_content)

    # Update entity/models.py for Django auto-discovery
    models_file = entity_dir / "models.py"
    if models_file.exists():
        models_content = models_file.read_text()
        import_line = f"from .{endpoint_name} import {model_name}"
        if import_line not in models_content:
            models_content += f"\n{import_line}\n"
            models_file.write_text(models_content)
    else:
        models_file.write_text(f"from .{endpoint_name} import {model_name}\n")

    # Create controller
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

    total = {model_name}.count()
    items = {model_name}.find_many()[offset : offset + limit]

    return {{
        "data": [
            {{
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "created_at": item.created_at.isoformat(),
            }}
            for item in items
        ],
        "pagination": {{"page": page, "limit": limit, "total": total}},
    }}


def get_by_id(req, id):
    """Get by ID"""
    item = {model_name}.find_unique(id=id)
    if not item:
        return Response().status_code(404).json({{"error": "Not found"}})
    
    return {{
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "created_at": item.created_at.isoformat(),
    }}


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
    
    item = {model_name}.find_unique(id=id)
    if not item:
        return Response().status_code(404).json({{"error": "Not found"}})
    
    data = req.body
    item.update_self(
        title=data.get("title", item.title),
        description=data.get("description", item.description),
    )
    return {{"message": "Updated"}}


def delete(req, id):
    """Delete"""
    if not req.user.is_authenticated:
        return Response().status_code(401).json({{"error": "Auth required"}})
    
    item = {model_name}.find_unique(id=id)
    if not item:
        return Response().status_code(404).json({{"error": "Not found"}})
    
    item.delete_self()
    return {{"message": "Deleted"}}
'''
    controller_file.write_text(controller_content)

    # Create routes with grouping
    routes_dir = Path("internal/routes")
    routes_file = routes_dir / f"{endpoint_name}.py"
    routes_content = f'''"""
{model_name} Routes
"""
from shanks import App
from internal.controller import {endpoint_name} as controller

# Create router
router = App()

# Group routes under /api/{endpoint_plural}
routes = router.group('api/{endpoint_plural}')


@routes.get('')
def list_{endpoint_plural}(req):
    """List all {endpoint_plural} with pagination"""
    return controller.list_{endpoint_plural}(req)


@routes.get('<id>')
def get_{endpoint_name}(req, id):
    """Get {endpoint_name} by ID"""
    return controller.get_by_id(req, id)


@routes.post('')
def create_{endpoint_name}(req):
    """Create new {endpoint_name}"""
    return controller.create(req)


@routes.put('<id>')
def update_{endpoint_name}(req, id):
    """Update {endpoint_name}"""
    return controller.update(req, id)


@routes.delete('<id>')
def delete_{endpoint_name}(req, id):
    """Delete {endpoint_name}"""
    return controller.delete(req, id)


# Include group routes to router
router.include(routes)
'''
    routes_file.write_text(routes_content)

    print(f"\n✅ CRUD created!")
    print(f"\n📁 Files:")
    print(f"  ├── entity/{endpoint_name}.py")
    print(f"  ├── internal/controller/{endpoint_name}.py")
    print(f"  └── internal/routes/{endpoint_name}.py")
    print(f"\n📝 Next steps:")
    print(f"   1. Import in internal/routes/__init__.py:")
    print(f"      from . import {endpoint_name}")
    print(f"      app.include({endpoint_name}.router)")
    print(f"   2. Run migrations:")
    print(f"      sorm db push")
    print(f"\n🎯 Endpoints:")
    print(f"  GET    /api/{endpoint_plural}")
    print(f"  GET    /api/{endpoint_plural}/<id>")
    print(f"  POST   /api/{endpoint_plural}")
    print(f"  PUT    /api/{endpoint_plural}/<id>")
    print(f"  DELETE /api/{endpoint_plural}/<id>")


def create_auth_endpoint():
    """Create authentication endpoints"""
    if len(sys.argv) < 4:
        print("Usage: shanks create auth --simple|--complete")
        sys.exit(1)

    auth_type = sys.argv[3]
    if auth_type not in ["--simple", "--complete"]:
        print("❌ Use --simple or --complete")
        sys.exit(1)

    if not Path("manage.py").exists():
        print("❌ Not in a Shanks project!")
        sys.exit(1)

    routes_dir = Path("internal/routes")
    auth_file = routes_dir / "auth.py"

    if auth_type == "--simple":
        auth_content = '''"""Auth Routes - Simple"""
from shanks import App, Response
from SORM import User, authenticate

# Create router
router = App()

# Group auth routes under /api/auth
auth = router.group('api/auth')


@auth.post('register')
def register(req):
    """Register new user"""
    data = req.body
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return Response().status_code(400).json({"error": "All fields required"})

    if User.find_unique(username=username):
        return Response().status_code(400).json({"error": "Username exists"})

    user = User.create(username=username, email=email, password=password)
    return Response().status_code(201).json({"message": "Registered", "user_id": user.id})


@auth.post('login')
def login(req):
    """Login user"""
    data = req.body
    user = authenticate(username=data.get("username"), password=data.get("password"))
    
    if not user:
        return Response().status_code(401).json({"error": "Invalid credentials"})
    
    return {"message": "Login successful", "user_id": user.id}


@auth.get('me')
def get_me(req):
    """Get current user"""
    if not req.user.is_authenticated:
        return Response().status_code(401).json({"error": "Not authenticated"})
    
    return {"id": req.user.id, "username": req.user.username, "email": req.user.email}


# Include group routes to router
router.include(auth)
'''
    else:  # --complete
        auth_content = '''"""Auth Routes - Complete"""
from shanks import App, Response
from SORM import User, authenticate

# Create router
router = App()

# Group auth routes under /api/auth
auth = router.group('api/auth')


@auth.post('register')
def register(req):
    """Register new user"""
    data = req.body
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return Response().status_code(400).json({"error": "All fields required"})

    if User.find_unique(username=username):
        return Response().status_code(400).json({"error": "Username exists"})

    user = User.create(username=username, email=email, password=password, is_active=False)
    # TODO: Send verification email
    return Response().status_code(201).json({"message": "Check email to verify"})


@auth.post('verify')
def verify_email(req):
    """Verify email"""
    token = req.body.get("token")
    # TODO: Implement verification
    return {"message": "Email verified"}


@auth.post('login')
def login(req):
    """Login user"""
    data = req.body
    user = authenticate(username=data.get("username"), password=data.get("password"))
    
    if not user:
        return Response().status_code(401).json({"error": "Invalid credentials"})
    
    if not user.is_active:
        return Response().status_code(403).json({"error": "Account not verified"})
    
    return {"message": "Login successful", "user_id": user.id}


@auth.get('me')
def get_me(req):
    """Get current user"""
    if not req.user.is_authenticated:
        return Response().status_code(401).json({"error": "Not authenticated"})
    
    return {"id": req.user.id, "username": req.user.username, "email": req.user.email}


# Include group routes to router
router.include(auth)
'''

    auth_file.write_text(auth_content)

    endpoints = ["POST /api/auth/register", "POST /api/auth/login", "GET  /api/auth/me"]
    if auth_type == "--complete":
        endpoints.insert(2, "POST /api/auth/verify")

    print(f"\n✅ Auth created!")
    print(f"\n📁 File: internal/routes/auth.py")
    print(f"\n📝 Import in internal/routes/__init__.py:")
    print(f"   from . import auth")
    print(f"   app.include(auth.router)")
    print(f"\n🎯 Endpoints:")
    for e in endpoints:
        print(f"  {e}")


def sorm_make():
    """Create migrations (like makemigrations)"""
    if not Path("manage.py").exists():
        print("❌ manage.py not found!")
        sys.exit(1)

    print("🔨 Creating migrations...")

    # Suppress Django output
    result = subprocess.run(
        [sys.executable, "manage.py", "makemigrations"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode == 0:
        # Only show relevant output
        output = result.stdout
        if "No changes detected" in output:
            print("✅ No changes detected")
        else:
            # Show migration files created
            for line in output.split("\n"):
                if (
                    "Migrations for" in line
                    or "Create model" in line
                    or "Add field" in line
                    or "Alter field" in line
                ):
                    print(f"  {line.strip()}")
            print("✅ Migrations created!")
    else:
        print("❌ Failed to create migrations")
        print(result.stderr)
        sys.exit(1)


def sorm_db_migrate():
    """Apply migrations to database"""
    if not Path("manage.py").exists():
        print("❌ manage.py not found!")
        sys.exit(1)

    print("🚀 Applying migrations...")

    result = subprocess.run(
        [sys.executable, "manage.py", "migrate"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode == 0:
        # Only show relevant output
        output = result.stdout
        for line in output.split("\n"):
            if "Applying" in line or "No migrations" in line:
                print(f"  {line.strip()}")
        print("✅ Migrations applied!")
    else:
        print("❌ Failed to apply migrations")
        print(result.stderr)
        sys.exit(1)


def sorm_db_push():
    """Create and apply migrations in one step"""
    if not Path("manage.py").exists():
        print("❌ manage.py not found!")
        sys.exit(1)

    print("🔨 Creating migrations...")
    result = subprocess.run(
        [sys.executable, "manage.py", "makemigrations"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        print("❌ Failed to create migrations")
        print(result.stderr)
        sys.exit(1)

    output = result.stdout
    if "No changes detected" in output:
        print("✅ No changes detected")
    else:
        for line in output.split("\n"):
            if "Migrations for" in line or "Create model" in line:
                print(f"  {line.strip()}")
        print("✅ Migrations created!")

    print("🚀 Applying migrations...")
    result = subprocess.run(
        [sys.executable, "manage.py", "migrate"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode == 0:
        output = result.stdout
        for line in output.split("\n"):
            if "Applying" in line:
                print(f"  {line.strip()}")
        print("✅ Database updated!")
    else:
        print("❌ Failed to apply migrations")
        print(result.stderr)
        sys.exit(1)


def sorm_db_reset():
    """Reset database (flush all data)"""
    if not Path("manage.py").exists():
        print("❌ manage.py not found!")
        sys.exit(1)

    print("⚠️  This will delete all data!")
    confirm = input("Type 'yes' to confirm: ")

    if confirm.lower() != "yes":
        print("❌ Cancelled")
        sys.exit(0)

    print("🗑️  Flushing database...")
    result = subprocess.run([sys.executable, "manage.py", "flush", "--noinput"])

    if result.returncode == 0:
        print("✅ Database reset!")
    else:
        print("❌ Failed to reset database")
        sys.exit(1)


def sorm_db_shell():
    """Open database shell"""
    if not Path("manage.py").exists():
        print("❌ manage.py not found!")
        sys.exit(1)

    print("🐚 Opening database shell...")
    subprocess.run([sys.executable, "manage.py", "dbshell"])


def sorm_studio():
    """Open Django admin (like Prisma Studio)"""
    if not Path("manage.py").exists():
        print("❌ manage.py not found!")
        sys.exit(1)

    print("🎨 Creating superuser for admin...")
    print("📝 Follow the prompts:\n")

    result = subprocess.run([sys.executable, "manage.py", "createsuperuser"])

    if result.returncode == 0:
        print("\n✅ Superuser created!")
        print("🚀 Starting Shanks server...")
        print("📊 Admin: http://127.0.0.1:8000/admin\n")

        try:
            subprocess.run([sys.executable, "manage.py", "runserver"])
        except KeyboardInterrupt:
            print("\n⏹️  Server stopped")


def show_sorm_help():
    """Show SORM help message"""
    help_text = """
SORM - Shanks ORM CLI (Prisma-like)

Usage:
    sorm <command> [options]

Commands:
    make                         Create migrations
                                 Like: prisma migrate dev --create-only

    db migrate                   Apply migrations to database
                                 Like: prisma migrate deploy

    db push                      Create and apply migrations (recommended)
                                 Like: prisma db push

    db reset                     Reset database (flush all data)
                                 Requires confirmation

    db shell                     Open interactive database shell

    studio                       Create superuser and open admin panel
                                 Like: prisma studio

Examples:
    sorm make                    # Create migrations
    sorm db migrate              # Apply migrations
    sorm db push                 # Create + apply (one command)
    sorm db reset                # Reset database
    sorm studio                  # Open admin panel
"""
    print(help_text)


def generate_django_structure():
    """Generate full Django project structure from Shanks project"""
    if not Path("manage.py").exists():
        print("❌ Not in a Shanks project directory!")
        print("Run this command from your Shanks project root.")
        sys.exit(1)

    print("🔨 Generating full Django structure...")
    print(
        "This will create a 'django_output' directory with standard Django structure.\n"
    )

    # Create output directory
    output_dir = Path("django_output")
    if output_dir.exists():
        print("⚠️  django_output directory already exists!")
        confirm = input("Overwrite? (yes/no): ")
        if confirm.lower() != "yes":
            print("❌ Cancelled")
            sys.exit(0)
        import shutil

        shutil.rmtree(output_dir)

    output_dir.mkdir()

    # Detect project name from settings
    settings_files = list(Path(".").glob("*/settings.py"))
    if not settings_files:
        print("❌ Could not find Django settings.py!")
        sys.exit(1)

    project_name = settings_files[0].parent.name
    print(f"📦 Project name: {project_name}")

    # Create Django project structure
    project_dir = output_dir / project_name
    project_dir.mkdir()

    # Copy settings.py
    print("📄 Copying settings.py...")
    settings_src = Path(project_name) / "settings.py"
    settings_dst = project_dir / "settings.py"
    if settings_src.exists():
        import shutil

        shutil.copy2(settings_src, settings_dst)

    # Copy wsgi.py
    print("📄 Copying wsgi.py...")
    wsgi_src = Path(project_name) / "wsgi.py"
    wsgi_dst = project_dir / "wsgi.py"
    if wsgi_src.exists():
        import shutil

        shutil.copy2(wsgi_src, wsgi_dst)

    # Copy asgi.py if exists
    asgi_src = Path(project_name) / "asgi.py"
    if asgi_src.exists():
        print("📄 Copying asgi.py...")
        import shutil

        shutil.copy2(asgi_src, project_dir / "asgi.py")

    # Create __init__.py
    (project_dir / "__init__.py").write_text("")

    # Generate urls.py from Shanks routes
    print("🔗 Generating urls.py from Shanks routes...")
    urls_content = generate_urls_from_shanks(project_name)
    (project_dir / "urls.py").write_text(urls_content)

    # Copy all apps (entity, dto, internal, etc.)
    print("📦 Copying application modules...")
    for app_dir in ["entity", "dto", "internal", "config", "utils"]:
        src = Path(app_dir)
        if src.exists() and src.is_dir():
            import shutil

            dst = output_dir / app_dir
            shutil.copytree(src, dst)
            print(f"  ✓ {app_dir}/")

    # Copy manage.py
    print("📄 Copying manage.py...")
    manage_src = Path("manage.py")
    if manage_src.exists():
        import shutil

        shutil.copy2(manage_src, output_dir / "manage.py")

    # Copy migrations
    print("📦 Copying migrations...")
    for app_dir in ["entity", "internal"]:
        migrations_src = Path(app_dir) / "migrations"
        if migrations_src.exists():
            import shutil

            migrations_dst = output_dir / app_dir / "migrations"
            if not migrations_dst.parent.exists():
                migrations_dst.parent.mkdir(parents=True)
            shutil.copytree(migrations_src, migrations_dst, dirs_exist_ok=True)
            print(f"  ✓ {app_dir}/migrations/")

    # Copy static and media if exists
    for dir_name in ["static", "staticfiles", "media"]:
        src = Path(dir_name)
        if src.exists():
            import shutil

            dst = output_dir / dir_name
            shutil.copytree(src, dst)
            print(f"  ✓ {dir_name}/")

    # Copy templates if exists
    templates_src = Path("templates")
    if templates_src.exists():
        import shutil

        shutil.copytree(templates_src, output_dir / "templates")
        print(f"  ✓ templates/")

    # Copy .env files
    for env_file in [".env", ".env.example"]:
        src = Path(env_file)
        if src.exists():
            import shutil

            shutil.copy2(src, output_dir / env_file)
            print(f"  ✓ {env_file}")

    # Copy requirements files
    for req_file in ["requirements.txt", "requirements-dev.txt"]:
        src = Path(req_file)
        if src.exists():
            import shutil

            shutil.copy2(src, output_dir / req_file)
            print(f"  ✓ {req_file}")

    # Generate README for Django output
    readme_content = f"""# {project_name} - Django Structure

This is the standard Django structure generated from your Shanks project.

## Structure

```
{project_name}/
├── {project_name}/        # Django settings
│   ├── settings.py
│   ├── urls.py           # Generated from Shanks routes
│   └── wsgi.py
├── entity/               # Django models
├── internal/             # Application code
├── manage.py
└── requirements.txt
```

## Deployment

This structure is ready for standard Django deployment:

### Using Gunicorn

```bash
pip install gunicorn
gunicorn {project_name}.wsgi:application
```

### Using uWSGI

```bash
pip install uwsgi
uwsgi --http :8000 --module {project_name}.wsgi
```

### Using Docker

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "{project_name}.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Environment Variables

Make sure to set:
- `SECRET_KEY`
- `DEBUG=False` (for production)
- `ALLOWED_HOSTS`
- Database settings

## Running Locally

```bash
python manage.py migrate
python manage.py runserver
```

## Comparison with Shanks

- Shanks version: Uses `internal/routes/__init__.py` with auto-generated urlpatterns
- Django version: Uses `{project_name}/urls.py` with explicit URL patterns

Both versions are functionally identical, but the Django version is more familiar
for traditional Django deployment tools and hosting platforms.
"""
    (output_dir / "README.md").write_text(readme_content)

    print("\n✅ Django structure generated successfully!")
    print(f"\n📁 Output directory: django_output/")
    print(f"\n📋 Structure:")
    print(f"  django_output/")
    print(f"  ├── {project_name}/")
    print(f"  │   ├── settings.py")
    print(f"  │   ├── urls.py        # Generated from Shanks routes")
    print(f"  │   └── wsgi.py")
    print(f"  ├── entity/            # Your models")
    print(f"  ├── internal/          # Your app code")
    print(f"  ├── manage.py")
    print(f"  └── README.md")
    print(f"\n🚀 Ready for deployment!")
    print(f"\n💡 Compare with your Shanks version:")
    print(f"   diff -r . django_output/")


def generate_urls_from_shanks(project_name):
    """Generate Django urls.py from Shanks routes"""
    # Try to import and inspect the routes
    try:
        import sys
        import importlib.util

        # Add current directory to path
        sys.path.insert(0, str(Path.cwd()))

        # Try to load routes module
        routes_path = Path("internal/routes/__init__.py")
        if not routes_path.exists():
            # Fallback to basic urls.py
            return f'''"""
URL Configuration for {project_name}
Generated from Shanks routes
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Add your URL patterns here
]
'''

        # Load the routes module
        spec = importlib.util.spec_from_file_location("routes", routes_path)
        routes_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(routes_module)

        # Get the app instance
        if hasattr(routes_module, "app"):
            app = routes_module.app
            # Get URL patterns from app
            urlpatterns = app.get_urls()

            # Generate urls.py content
            urls_content = f'''"""
URL Configuration for {project_name}
Generated from Shanks routes
"""
from django.contrib import admin
from django.urls import path, include

# Import your routes
from internal.routes import app

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Add Shanks routes
urlpatterns += app.get_urls()
'''
            return urls_content

    except Exception as e:
        print(f"⚠️  Could not auto-generate URLs: {e}")
        print("   Creating basic urls.py template...")

    # Fallback template
    return f'''"""
URL Configuration for {project_name}
Generated from Shanks routes
"""
from django.contrib import admin
from django.urls import path, include

# Import your routes
from internal.routes import app

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Add Shanks routes
urlpatterns += app.get_urls()
'''


def show_help():
    """Show help message"""
    help_text = """
Shanks Django CLI

Usage:
    shanks <command> [options]

Commands:
    run [host:port]              Run development server with auto-reload
                                 Default: 127.0.0.1:8000

    new <name>                   Create a new Shanks Django project
                                 with Go-like architecture

    create <endpoint> --crud     Generate CRUD endpoints with model
                                 Creates: entity, controller, routes
                                 Example: shanks create products --crud

    create auth --simple         Generate simple auth endpoints
                                 Creates: /login, /register, /me

    create auth --complete       Generate complete auth endpoints
                                 Creates: /login, /register, /verify, /me

    generate django              Generate full Django project structure
                                 Creates: django_output/ with standard Django layout
                                 Useful for deployment or comparison

    format                       Format code with black
    lint                         Lint code with flake8
    check                        Format and lint code

    help                         Show this help message

Database Commands (use 'sorm' CLI):
    sorm make                    Create migrations
    sorm db migrate              Apply migrations
    sorm db push                 Create + apply migrations
    sorm db reset                Reset database
    sorm db shell                Database shell
    sorm studio                  Open admin panel

Examples:
    shanks new myproject                # Create new project
    shanks create products --crud       # Generate products CRUD
    shanks create auth --simple         # Generate auth endpoints
    shanks generate django              # Generate Django structure
    shanks run                          # Start server
    shanks format                       # Format code
    
    sorm db push                        # Database migrations
    sorm studio                         # Open admin panel
"""
    print(help_text)


def sorm_main():
    """Main entry point for SORM CLI"""
    if len(sys.argv) < 2:
        show_sorm_help()
        sys.exit(0)

    command = sys.argv[1]

    if command == "make":
        sorm_make()
    elif command == "db":
        if len(sys.argv) < 3:
            print("Usage: sorm db <action>")
            print("Actions: migrate, push, reset, shell")
            sys.exit(1)

        action = sys.argv[2]
        if action == "migrate":
            sorm_db_migrate()
        elif action == "push":
            sorm_db_push()
        elif action == "reset":
            sorm_db_reset()
        elif action == "shell":
            sorm_db_shell()
        else:
            print(f"Unknown db action: {action}")
            print("Use: migrate, push, reset, or shell")
            sys.exit(1)
    elif command == "studio":
        sorm_studio()
    elif command == "help" or command == "--help" or command == "-h":
        show_sorm_help()
    else:
        print(f"Unknown command: {command}")
        show_sorm_help()
        sys.exit(1)


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    command = sys.argv[1]

    if command == "run":
        run_server()
    elif command == "new":
        create_project()
    elif command == "create":
        # Handle create subcommands
        if len(sys.argv) < 3:
            print("Usage: shanks create <endpoint> --crud")
            print("       shanks create auth --simple|--complete")
            sys.exit(1)

        subcommand = sys.argv[2]
        if subcommand == "auth":
            create_auth_endpoint()
        elif "--crud" in sys.argv:
            create_crud_endpoint()
        else:
            print(f"Unknown create command: {subcommand}")
            print("Use: shanks create <endpoint> --crud")
            print("Or:  shanks create auth --simple|--complete")
            sys.exit(1)
    elif command == "format":
        format_code()
    elif command == "lint":
        lint_code()
    elif command == "check":
        format_code()
        lint_code()
    elif command == "generate":
        # Handle generate subcommands
        if len(sys.argv) < 3:
            print("Usage: shanks generate <type>")
            print("Types: django")
            sys.exit(1)

        subcommand = sys.argv[2]
        if subcommand == "django":
            generate_django_structure()
        else:
            print(f"Unknown generate type: {subcommand}")
            print("Use: shanks generate django")
            sys.exit(1)
    elif command == "help":
        show_help()
    else:
        print(f"Unknown command: {command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
