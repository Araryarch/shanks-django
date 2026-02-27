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

    for subdir in ["controller", "repository", "service", "middleware", "routes"]:
        dir_path = internal_dir / subdir
        dir_path.mkdir(exist_ok=True)
        (dir_path / "__init__.py").write_text("", encoding="utf-8")

    for dir_name in ["dto", "entity", "config", "utils"]:
        dir_path = project_dir / dir_name
        dir_path.mkdir(exist_ok=True)
        (dir_path / "__init__.py").write_text("", encoding="utf-8")

    # Create base DTO
    print("[2/5] Creating base DTO and routes...")
    (project_dir / "dto" / "base_dto.py").write_text(
        get_base_dto_template(), encoding="utf-8"
    )
    
    # Create health route file
    (internal_dir / "routes" / "health_route.py").write_text(
        get_health_route_template(project_name), encoding="utf-8"
    )
    
    # Create routes __init__.py
    (internal_dir / "routes" / "__init__.py").write_text(
        get_routes_init_template(), encoding="utf-8"
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
    print_banner()
    print("Starting Shanks development server...\n")
    
    try:
        subprocess.run(
            [sys.executable, "manage.py", "runserver"],
            check=True
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except FileNotFoundError:
        print("[ERROR] manage.py not found. Are you in a Shanks project directory?")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Server failed to start: {e}")
        sys.exit(1)
