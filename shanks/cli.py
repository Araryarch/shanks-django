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

    # Create api.py with example
    api_content = '''"""API routes for {project_name}"""
from shanks import App, Response

app = App()


@app.get("api/hello")
def hello(req):
    """Hello World endpoint"""
    return {{"message": "Hello from Shanks Django!"}}


@app.get("api/health")
def health(req):
    """Health check endpoint"""
    return {{"status": "ok", "framework": "shanks-django"}}


# Export URL patterns
urlpatterns = app.get_urls()
'''.format(project_name=project_name)

    api_file = Path(project_name) / project_name / "api.py"
    api_file.write_text(api_content)

    # Update urls.py
    urls_file = Path(project_name) / project_name / "urls.py"
    urls_content = '''"""URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from . import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(api.urlpatterns)),
]
'''
    urls_file.write_text(urls_content)

    print(f"\n✅ Project created successfully!")
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    print(f"  shanks run")
    print(f"\nThen visit: http://127.0.0.1:8000/api/hello")


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
