"""CRUD generation command"""

import sys
from pathlib import Path

from .crud_templates import *


def create_crud_endpoint():
    """Generate CRUD endpoint with full layered architecture"""
    if len(sys.argv) < 3:
        print("Usage: shanks create <endpoint_name> --crud")
        sys.exit(1)

    endpoint_name = sys.argv[2]

    # Check if --crud flag is present
    if "--crud" not in sys.argv:
        print("Error: --crud flag is required")
        print("Usage: shanks create <endpoint_name> --crud")
        sys.exit(1)

    # Convert endpoint name to model name (capitalize first letter)
    model_name = endpoint_name.capitalize()

    # Pluralize endpoint name (simple pluralization)
    endpoint_plural = (
        endpoint_name + "s" if not endpoint_name.endswith("s") else endpoint_name
    )

    print(f"\nGenerating CRUD endpoint: {endpoint_name}")
    print(f"Model: {model_name}")
    print(f"Endpoint: /api/{endpoint_plural}\n")

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
        get_repository_template(model_name, endpoint_name), encoding="utf-8"
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
        get_service_template(model_name, endpoint_name, endpoint_plural),
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
        get_controller_template(model_name, endpoint_name, endpoint_plural),
        encoding="utf-8",
    )

    # Update controller __init__.py
    controller_init_file = controller_dir / "__init__.py"
    controller_init_content = controller_init_file.read_text(encoding="utf-8")
    import_line = f"from . import {endpoint_name}_controller"
    if import_line not in controller_init_content:
        controller_init_content += f"\n{import_line}\n"
        controller_init_file.write_text(controller_init_content, encoding="utf-8")

    # [5/5] Create views
    print("[5/5] Creating views...")
    views_dir = Path("internal/views")
    views_dir.mkdir(parents=True, exist_ok=True)
    if not (views_dir / "__init__.py").exists():
        (views_dir / "__init__.py").write_text("", encoding="utf-8")

    view_file = views_dir / f"{endpoint_name}_view.py"
    view_file.write_text(
        get_route_template(model_name, endpoint_name, endpoint_plural), encoding="utf-8"
    )

    # Auto-register views in __init__.py
    print("[6/6] Auto-registering views...")
    views_init_file = views_dir / "__init__.py"

    if views_init_file.exists():
        views_init_content = views_init_file.read_text(encoding="utf-8")

        # Add import if not exists
        import_line = (
            f"from .{endpoint_name}_view import router as {endpoint_name}_router"
        )
        if import_line not in views_init_content:
            # Find where to insert import (after existing imports or after app definition)
            lines = views_init_content.split("\n")
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
            views_init_content = "\n".join(lines)

        # Update urlpatterns line - support both old and new format
        if "urlpatterns = [*health_router]" in views_init_content:
            # First CRUD after health router
            views_init_content = views_init_content.replace(
                "urlpatterns = [*health_router]",
                f"urlpatterns = [*health_router, *{endpoint_name}_router]",
            )
        elif "urlpatterns = [*app]" in views_init_content:
            # Old format with app - convert to new format
            views_init_content = views_init_content.replace(
                "urlpatterns = [*app]",
                f"urlpatterns = [*health_router, *{endpoint_name}_router]",
            )
        elif "urlpatterns = [*app.get_urls()]" in views_init_content:
            # Old format with get_urls() - convert to new format
            views_init_content = views_init_content.replace(
                "urlpatterns = [*app.get_urls()]",
                f"urlpatterns = [*health_router, *{endpoint_name}_router]",
            )
        elif "urlpatterns = app.get_urls()" in views_init_content:
            # Very old format - convert to new format
            views_init_content = views_init_content.replace(
                "urlpatterns = app.get_urls()",
                f"urlpatterns = [*health_router, *{endpoint_name}_router]",
            )
        elif f"*{endpoint_name}_router" not in views_init_content:
            # Already has routers, add new one before closing bracket
            views_init_content = views_init_content.replace(
                "urlpatterns = [",
                f"urlpatterns = [*health_router, *{endpoint_name}_router, ",
            ).replace("[*health_router, *health_router", "[*health_router")

        views_init_file.write_text(views_init_content, encoding="utf-8")
        print(f"  ✓ Updated internal/views/__init__.py")
    else:
        print(f"  ✗ internal/views/__init__.py not found")

    print(f"\n✓ CRUD endpoint '{endpoint_name}' created successfully!")
    print(f"\nGenerated files:")
    print(f"  - db/entity/{endpoint_name}_entity.py")
    print(f"  - internal/repository/{endpoint_name}_repository.py")
    print(f"  - internal/service/{endpoint_name}_service.py")
    print(f"  - internal/controller/{endpoint_name}_controller.py")
    print(f"  - internal/views/{endpoint_name}_view.py")
    print(f"\nEndpoints:")
    print(f"  GET    /api/{endpoint_plural}")
    print(f"  GET    /api/{endpoint_plural}/<id>")
    print(f"  POST   /api/{endpoint_plural}")
    print(f"  PUT    /api/{endpoint_plural}/<id>")
    print(f"  DELETE /api/{endpoint_plural}/<id>")
    print(f"\nNext steps:")
    print(f"  sorm db push   # Apply database changes")
    print(f"  sorm db seed   # Run seeders (optional)")
