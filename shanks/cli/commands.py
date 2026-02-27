"""CLI command implementations"""

import subprocess
import sys
from pathlib import Path

from .banner import print_banner
from .templates import *
from .crud_templates import *


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
            text=True,
        )
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("[INFO] Installing Django...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "django"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        result = subprocess.run(
            [sys.executable, "-m", "django", "startproject", project_name],
            check=False,
            capture_output=True,
            text=True,
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
    (internal_dir / "__init__.py").write_text("", encoding="utf-8")

    for subdir in ["controller", "repository", "service", "middleware", "views"]:
        dir_path = internal_dir / subdir
        dir_path.mkdir(exist_ok=True)
        (dir_path / "__init__.py").write_text("", encoding="utf-8")

    # Create db structure
    db_dir = project_dir / "db"
    db_dir.mkdir(exist_ok=True)
    (db_dir / "__init__.py").write_text("", encoding="utf-8")

    entity_dir = db_dir / "entity"
    entity_dir.mkdir(exist_ok=True)
    (entity_dir / "__init__.py").write_text("", encoding="utf-8")

    migrations_dir = db_dir / "migrations"
    migrations_dir.mkdir(exist_ok=True)
    (migrations_dir / "__init__.py").write_text("", encoding="utf-8")

    seeds_dir = db_dir / "seeds"
    seeds_dir.mkdir(exist_ok=True)
    (seeds_dir / "__init__.py").write_text("", encoding="utf-8")

    # Create example seed file
    example_seed = f'''"""
Example seed file
Run with: sorm db seed
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
django.setup()

from django.contrib.auth.models import User

# Example: Create admin user
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("✓ Admin user created")
else:
    print("ℹ Admin user already exists")
'''
    (seeds_dir / "example_seed.py").write_text(example_seed, encoding="utf-8")

    for dir_name in ["dto", "config", "utils"]:
        dir_path = project_dir / dir_name
        dir_path.mkdir(exist_ok=True)
        (dir_path / "__init__.py").write_text("", encoding="utf-8")

    # Create templates directory
    templates_dir = project_dir / "templates"
    templates_dir.mkdir(exist_ok=True)

    # Create example template
    (templates_dir / "index.html").write_text(
        get_index_template(project_name), encoding="utf-8"
    )

    # Create base DTO
    print("[2/5] Creating base DTO and views...")
    (project_dir / "dto" / "base_dto.py").write_text(
        get_base_dto_template(), encoding="utf-8"
    )

    # Create health view file
    (internal_dir / "views" / "health_view.py").write_text(
        get_health_view_template(project_name), encoding="utf-8"
    )

    # Create views __init__.py (routes)
    (internal_dir / "views" / "__init__.py").write_text(
        get_views_init_template(), encoding="utf-8"
    )

    # Create middleware
    (internal_dir / "middleware" / "logger.py").write_text(
        get_middleware_template(), encoding="utf-8"
    )

    # Update settings.py
    print("[3/5] Configuring Django settings...")
    (config_dir / "settings.py").write_text(
        get_settings_template(project_name), encoding="utf-8"
    )

    # Update wsgi.py
    (config_dir / "wsgi.py").write_text(
        get_wsgi_template(project_name), encoding="utf-8"
    )

    # Delete urls.py
    urls_file = config_dir / "urls.py"
    if urls_file.exists():
        urls_file.unlink()

    # Update manage.py
    print("[4/5] Creating management scripts...")
    (project_dir / "manage.py").write_text(
        get_manage_template(project_name), encoding="utf-8"
    )

    # Create .env.example
    (project_dir / ".env.example").write_text(
        get_env_example_template(), encoding="utf-8"
    )

    # Create README
    print("[5/5] Creating documentation...")
    (project_dir / "README.md").write_text(
        get_readme_template(project_name), encoding="utf-8"
    )

    print(f"\n✓ Project '{project_name}' created successfully!")
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    print(f"  cp .env.example .env")
    print(f"  sorm db push")
    print(f"  shanks run")


def run_server():
    """Run Django development server"""
    import os

    print_banner()
    print("Starting Shanks development server...")
    print("Server running at http://127.0.0.1:8000/")
    print("Press CTRL+C to stop\n")

    try:
        # Suppress Django startup messages by redirecting to devnull
        with open(os.devnull, "w") as devnull:
            process = subprocess.Popen(
                [sys.executable, "manage.py", "runserver"],
                stdout=devnull,
                stderr=subprocess.STDOUT,
                env={**os.environ, "PYTHONUNBUFFERED": "1"},
            )
            process.wait()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except FileNotFoundError:
        print("[ERROR] manage.py not found. Are you in a Shanks project directory?")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Server failed to start: {e}")
        sys.exit(1)
