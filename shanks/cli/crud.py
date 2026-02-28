"""CRUD generation command"""

import sys
from pathlib import Path

from .crud_templates import *


def create_crud_endpoint():
    """Generate CRUD endpoint with full layered architecture"""
    if len(sys.argv) < 3:
        print("Usage: shanks create <endpoint_name> [--crud|-c|-r|-u|-d] [--auth]")
        print("\nExamples:")
        print("  shanks create books              # Default: full CRUD")
        print("  shanks create books --crud       # Full CRUD")
        print("  shanks create books -c -r        # Only Create and Read")
        print("  shanks create books -c --auth    # Only Create with auth required")
        print("  shanks create books --crud --auth # Full CRUD, all protected")
        sys.exit(1)

    endpoint_name = sys.argv[2]

    # Parse flags
    has_crud_flag = "--crud" in sys.argv
    has_c = "-c" in sys.argv
    has_r = "-r" in sys.argv
    has_u = "-u" in sys.argv
    has_d = "-d" in sys.argv
    has_auth = "--auth" in sys.argv

    # Determine which operations to generate
    # Default: full CRUD if no flags specified
    if not (has_crud_flag or has_c or has_r or has_u or has_d):
        # Default behavior: full CRUD
        operations = {"create": True, "read": True, "update": True, "delete": True}
    elif has_crud_flag:
        # --crud flag: all operations
        operations = {"create": True, "read": True, "update": True, "delete": True}
    else:
        # Individual flags
        operations = {"create": has_c, "read": has_r, "update": has_u, "delete": has_d}

    # Convert endpoint name to model name (capitalize first letter)
    model_name = endpoint_name.capitalize()

    print(f"\nGenerating endpoint: {endpoint_name}")
    print(f"Model: {model_name}")
    print(f"Operations: {', '.join([k.upper() for k, v in operations.items() if v])}")
    if has_auth:
        print(f"Auth: Required for all operations")
    print(f"Endpoint: /api/v1/{endpoint_name}\n")

    # [1/5] Create entity (Django model)
    print("[1/5] Creating entity (Django model)...")
    entity_dir = Path("db/entity")
    entity_dir.mkdir(parents=True, exist_ok=True)
    if not (entity_dir / "__init__.py").exists():
        (entity_dir / "__init__.py").write_text("", encoding="utf-8")

    entity_file = entity_dir / f"{endpoint_name}_entity.py"
    entity_file.write_text(
        get_entity_template(model_name, endpoint_name), encoding="utf-8"
    )

    # Update models.py to import all entities
    models_file = entity_dir.parent / "models.py"
    if not models_file.exists():
        models_file.write_text("# Auto-generated models file\n", encoding="utf-8")

    models_content = models_file.read_text(encoding="utf-8")
    import_line = f"from .entity.{endpoint_name}_entity import {model_name}"
    if import_line not in models_content:
        models_content += f"{import_line}\n"
        models_file.write_text(models_content, encoding="utf-8")

    # [2/5] Create repository
    print("[2/5] Creating repository (data access)...")
    repository_dir = Path("internal/repository")
    repository_dir.mkdir(parents=True, exist_ok=True)
    if not (repository_dir / "__init__.py").exists():
        (repository_dir / "__init__.py").write_text("", encoding="utf-8")

    repository_file = repository_dir / f"{endpoint_name}_repository.py"
    repository_file.write_text(
        get_repository_template(model_name, endpoint_name, operations), encoding="utf-8"
    )

    # Update repository __init__.py
    repository_init_file = repository_dir / "__init__.py"
    repository_init_content = repository_init_file.read_text(encoding="utf-8")
    import_line = f"from . import {endpoint_name}_repository"
    if import_line not in repository_init_content:
        repository_init_content += f"\n{import_line}\n"
        repository_init_file.write_text(repository_init_content, encoding="utf-8")

    # [3/5] Create service
    print("[3/5] Creating service (business logic)...")
    service_dir = Path("internal/service")
    service_dir.mkdir(parents=True, exist_ok=True)
    if not (service_dir / "__init__.py").exists():
        (service_dir / "__init__.py").write_text("", encoding="utf-8")

    service_file = service_dir / f"{endpoint_name}_service.py"
    service_file.write_text(
        get_service_template(model_name, endpoint_name, endpoint_name, operations),
        encoding="utf-8",
    )

    # Update service __init__.py
    service_init_file = service_dir / "__init__.py"
    service_init_content = service_init_file.read_text(encoding="utf-8")
    import_line = f"from . import {endpoint_name}_service"
    if import_line not in service_init_content:
        service_init_content += f"\n{import_line}\n"
        service_init_file.write_text(service_init_content, encoding="utf-8")

    # [4/5] Create controller
    print("[4/5] Creating controller (request handling)...")
    controller_dir = Path("internal/controller")
    controller_dir.mkdir(parents=True, exist_ok=True)
    if not (controller_dir / "__init__.py").exists():
        (controller_dir / "__init__.py").write_text("", encoding="utf-8")

    controller_file = controller_dir / f"{endpoint_name}_controller.py"
    controller_file.write_text(
        get_controller_template(model_name, endpoint_name, endpoint_name, operations),
        encoding="utf-8",
    )

    # Update controller __init__.py
    controller_init_file = controller_dir / "__init__.py"
    controller_init_content = controller_init_file.read_text(encoding="utf-8")
    import_line = f"from . import {endpoint_name}_controller"
    if import_line not in controller_init_content:
        controller_init_content += f"\n{import_line}\n"
        controller_init_file.write_text(controller_init_content, encoding="utf-8")

    # [5/5] Create routes
    print("[5/5] Creating routes...")
    routes_dir = Path("internal/routes")
    routes_dir.mkdir(parents=True, exist_ok=True)
    if not (routes_dir / "__init__.py").exists():
        (routes_dir / "__init__.py").write_text("", encoding="utf-8")

    route_file = routes_dir / f"{endpoint_name}_route.py"
    route_file.write_text(
        get_route_template(
            model_name, endpoint_name, endpoint_name, operations, has_auth
        ),
        encoding="utf-8",
    )

    # Auto-register routes in __init__.py
    print("[6/6] Auto-registering routes...")
    routes_init_file = routes_dir / "__init__.py"

    if routes_init_file.exists():
        routes_init_content = routes_init_file.read_text(encoding="utf-8")

        # Add import if not exists
        import_line = (
            f"from .{endpoint_name}_route import router as {endpoint_name}_router"
        )
        if import_line not in routes_init_content:
            # Find where to insert import (after existing imports or after app definition)
            lines = routes_init_content.split("\n")
            insert_index = 0

            # Find last import or app definition
            for i, line in enumerate(lines):
                if line.startswith("from .") and "_router" in line:
                    insert_index = i + 1
                elif "app = App()" in line:
                    insert_index = i + 1

            # Insert blank line if needed
            if insert_index > 0 and lines[insert_index].strip():
                lines.insert(insert_index, "")
                insert_index += 1

            lines.insert(insert_index, import_line)
            routes_init_content = "\n".join(lines)

        # Update urlpatterns line - support both old and new format
        if "urlpatterns = [*health_router]" in routes_init_content:
            # First CRUD after health router
            routes_init_content = routes_init_content.replace(
                "urlpatterns = [*health_router]",
                f"urlpatterns = [*health_router, *{endpoint_name}_router]",
            )
        elif "urlpatterns = [*app]" in routes_init_content:
            # Old format with app - convert to new format
            routes_init_content = routes_init_content.replace(
                "urlpatterns = [*app]",
                f"urlpatterns = [*health_router, *{endpoint_name}_router]",
            )
        elif "urlpatterns = [*app.get_urls()]" in routes_init_content:
            # Old format with get_urls() - convert to new format
            routes_init_content = routes_init_content.replace(
                "urlpatterns = [*app.get_urls()]",
                f"urlpatterns = [*health_router, *{endpoint_name}_router]",
            )
        elif "urlpatterns = app.get_urls()" in routes_init_content:
            # Very old format - convert to new format
            routes_init_content = routes_init_content.replace(
                "urlpatterns = app.get_urls()",
                f"urlpatterns = [*health_router, *{endpoint_name}_router]",
            )
        elif f"*{endpoint_name}_router" not in routes_init_content:
            # Already has routers, add new one before closing bracket
            import re

            routes_init_content = re.sub(
                r"urlpatterns = \[(.*?)\]",
                lambda m: f"urlpatterns = [{m.group(1)}, *{endpoint_name}_router]",
                routes_init_content,
            )

        routes_init_file.write_text(routes_init_content, encoding="utf-8")
        print(f"  ✓ Updated internal/routes/__init__.py")
    else:
        print(f"  ✗ internal/routes/__init__.py not found")

    print(f"\n✓ Endpoint '{endpoint_name}' created successfully!")
    print(f"\nGenerated files:")
    print(f"  - db/entity/{endpoint_name}_entity.py")
    print(f"  - internal/repository/{endpoint_name}_repository.py")
    print(f"  - internal/service/{endpoint_name}_service.py")
    print(f"  - internal/controller/{endpoint_name}_controller.py")
    print(f"  - internal/routes/{endpoint_name}_route.py")
    print(f"\nEndpoints:")
    if operations["read"]:
        auth_marker = " 🔒" if has_auth else ""
        print(f"  GET    /api/v1/{endpoint_name}{auth_marker}")
        print(f"  GET    /api/v1/{endpoint_name}/<id>{auth_marker}")
    if operations["create"]:
        auth_marker = " 🔒" if has_auth else ""
        print(f"  POST   /api/v1/{endpoint_name}{auth_marker}")
    if operations["update"]:
        auth_marker = " 🔒" if has_auth else ""
        print(f"  PUT    /api/v1/{endpoint_name}/<id>{auth_marker}")
    if operations["delete"]:
        auth_marker = " 🔒" if has_auth else ""
        print(f"  DELETE /api/v1/{endpoint_name}/<id>{auth_marker}")

    if has_auth:
        print(f"\n🔒 All endpoints require JWT authentication")

    print(f"\nNext steps:")
    print(f"  python manage.py makemigrations")
    print(f"  python manage.py migrate")
