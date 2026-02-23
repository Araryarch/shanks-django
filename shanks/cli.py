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
        print("Make sure you're in a Django project directory.")
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
    print(f"🔄 Auto-reload enabled (like nodemon)")
    print(f"⏹️  Press Ctrl+C to stop\n")

    # Run Django development server with auto-reload
    try:
        subprocess.run(
            [sys.executable, "manage.py", "runserver", f"{host}:{port}"],
            check=True,
        )
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)


def create_project():
    """Create a new Shanks Django project"""
    if len(sys.argv) < 3:
        print("Usage: shanks new <project_name>")
        sys.exit(1)

    project_name = sys.argv[2]
    print(f"🎉 Creating new Shanks project: {project_name}")

    # Create Django project
    try:
        subprocess.run(["django-admin", "startproject", project_name], check=True)
    except FileNotFoundError:
        print("❌ django-admin not found. Installing Django...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "django"])
        subprocess.run(["django-admin", "startproject", project_name], check=True)

    project_dir = Path(project_name)
    config_dir = project_dir / project_name

    # Create app directory
    app_dir = project_dir / "app"
    app_dir.mkdir(exist_ok=True)
    (app_dir / "__init__.py").write_text("")

    # Create routes directory
    routes_dir = app_dir / "routes"
    routes_dir.mkdir(exist_ok=True)

    # Create routes/__init__.py with example
    routes_content = '''"""API routes"""
from shanks import App

app = App()


@app.get("api/hello")
def hello(req):
    """Hello World endpoint"""
    return {"message": "Hello from Shanks Django!"}


@app.get("api/health")
def health(req):
    """Health check endpoint"""
    return {"status": "ok", "framework": "shanks-django"}


# Export URL patterns - No urls.py needed!
urlpatterns = app.get_urls()
'''
    (routes_dir / "__init__.py").write_text(routes_content)

    # Update settings.py with simplified config
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
INSTALLED_APPS = get_installed_apps(["app"])

# Middleware
MIDDLEWARE = get_middleware()

# Routing
ROOT_URLCONF = "app.routes"

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
    wsgi_content = '''"""WSGI - Auto-configured by Shanks"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{project_name}.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
'''.format(project_name=project_name)
    (config_dir / "wsgi.py").write_text(wsgi_content)

    # Delete urls.py (not needed anymore)
    urls_file = config_dir / "urls.py"
    if urls_file.exists():
        urls_file.unlink()

    # Create .env.example
    env_example = """# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=*

# Database (optional)
# DATABASE_URL=postgresql://user:pass@localhost/dbname
# DATABASE_URL=mysql://user:pass@localhost/dbname

# CORS (optional)
# CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
"""
    (project_dir / ".env.example").write_text(env_example)

    # Create README.md
    readme_content = """# {project_name}

Shanks Django project - Express.js-like API framework

## Quick Start

```bash
# Install dependencies
pip install shanks-django

# Run migrations
python manage.py migrate

# Start server
shanks run
```

Visit: http://127.0.0.1:8000/api/hello

## Project Structure

```
{project_name}/
├── {project_name}/
│   ├── settings.py    # Simplified settings
│   ├── wsgi.py       # Minimal WSGI
│   └── ...
├── app/
│   └── routes/
│       └── __init__.py  # Your routes here
├── manage.py
└── .env.example
```

## Add Routes

Edit `app/routes/__init__.py`:

```python
@app.get("api/users")
def list_users(req):
    return {{"users": []}}

@app.post("api/users")
def create_user(req):
    data = req.body
    return {{"created": True}}
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

## Learn More

- [Shanks Documentation](https://github.com/Ararya/shanks-django)
- [Routing Guide](https://github.com/Ararya/shanks-django#routing)
- [ORM Guide](https://github.com/Ararya/shanks-django#orm)
""".format(project_name=project_name)
    (project_dir / "README.md").write_text(readme_content)

    print(f"\n✅ Project created successfully!")
    print(f"\n📁 Project structure:")
    print(f"  {project_name}/")
    print(f"  ├── {project_name}/")
    print(f"  │   ├── settings.py    # Simplified with Shanks helpers")
    print(f"  │   ├── wsgi.py       # Minimal WSGI")
    print(f"  │   └── ...")
    print(f"  ├── app/")
    print(f"  │   └── routes/")
    print(f"  │       └── __init__.py  # Your routes here")
    print(f"  ├── manage.py")
    print(f"  ├── .env.example")
    print(f"  └── README.md")
    print(f"\n🚀 Next steps:")
    print(f"  cd {project_name}")
    print(f"  cp .env.example .env")
    print(f"  python manage.py migrate")
    print(f"  shanks run")
    print(f"\n🌐 Then visit: http://127.0.0.1:8000/api/hello")
    print(f"\n💡 No urls.py needed! Routes are in app/routes/__init__.py")


def show_help():
    """Show help message"""
    help_text = """
Shanks Django CLI

Usage:
    shanks <command> [options]

Commands:
    run [host:port]    Run development server with auto-reload (like nodemon)
                       Default: 127.0.0.1:8000
                       Examples:
                         shanks run
                         shanks run 8080
                         shanks run 0.0.0.0:3000

    new <name>         Create a new Shanks Django project

    format             Format code with black
    lint               Lint code with flake8
    check              Format and lint code

    help               Show this help message

Examples:
    shanks run                    # Start server on 127.0.0.1:8000
    shanks run 3000               # Start server on 127.0.0.1:3000
    shanks run 0.0.0.0:8000       # Start server on all interfaces
    shanks new myproject          # Create new project
    shanks format                 # Format code
    shanks check                  # Format and lint
"""
    print(help_text)


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
    elif command == "format":
        format_code()
    elif command == "lint":
        lint_code()
    elif command == "check":
        format_code()
        lint_code()
    elif command == "help":
        show_help()
    else:
        print(f"Unknown command: {command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
