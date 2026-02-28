"""Authentication generation command"""

import sys
from pathlib import Path
from .auth_templates import get_simple_auth_controller_template, get_simple_auth_route_template
from .auth_complete_templates import get_complete_auth_controller_template, get_complete_auth_route_template


def create_auth_endpoint():
    """Generate authentication endpoints (simple or complete)"""
    if len(sys.argv) < 3:
        print("Usage: shanks create auth --simple | --complete")
        sys.exit(1)

    # Check which flag is present
    is_simple = "--simple" in sys.argv
    is_complete = "--complete" in sys.argv

    if not is_simple and not is_complete:
        print("Error: --simple or --complete flag is required")
        print("Usage: shanks create auth --simple | --complete")
        sys.exit(1)

    if is_complete:
        create_complete_auth()
    else:
        create_simple_auth()


def create_simple_auth():
    """Generate simple authentication endpoints"""
    print("\nGenerating simple authentication endpoints...")
    print("Endpoints: /api/auth/login, /api/auth/register, /api/auth/logout\n")

    # [1/3] Create auth controller
    print("[1/3] Creating auth controller...")
    controller_dir = Path("internal/controller")
    controller_dir.mkdir(parents=True, exist_ok=True)
    if not (controller_dir / "__init__.py").exists():
        (controller_dir / "__init__.py").write_text("", encoding="utf-8")

    controller_file = controller_dir / "auth_controller.py"
    controller_file.write_text(get_simple_auth_controller_template(), encoding="utf-8")

    # Update controller __init__.py
    controller_init_file = controller_dir / "__init__.py"
    controller_init_content = controller_init_file.read_text(encoding="utf-8")
    import_line = "from . import auth_controller"
    if import_line not in controller_init_content:
        controller_init_content += f"\n{import_line}\n"
        controller_init_file.write_text(controller_init_content, encoding="utf-8")

    # [2/3] Create auth routes
    print("[2/3] Creating auth routes...")
    routes_dir = Path("internal/routes")
    routes_dir.mkdir(parents=True, exist_ok=True)
    if not (routes_dir / "__init__.py").exists():
        (routes_dir / "__init__.py").write_text("", encoding="utf-8")

    route_file = routes_dir / "auth_route.py"
    route_file.write_text(get_simple_auth_route_template(), encoding="utf-8")

    # [3/3] Auto-register routes
    print("[3/3] Auto-registering routes...")
    register_auth_routes()

    print(f"\n✓ Simple authentication endpoints created successfully!")
    print(f"\nGenerated files:")
    print(f"  - internal/controller/auth_controller.py")
    print(f"  - internal/routes/auth_route.py")
    print(f"\nEndpoints:")
    print(f"  POST   /api/v1/auth/register  - Register new user")
    print(f"  POST   /api/v1/auth/login     - Login user")
    print(f"  POST   /api/v1/auth/logout    - Logout user (client-side)")
    print(f"  GET    /api/v1/auth/me        - Get current user info")
    print(f"\nExample usage:")
    print(f'  Register: POST /api/v1/auth/register {{"username":"user","email":"user@test.com","password":"pass123"}}')
    print(f'  Response: {{"token": "eyJ...", "user": {{...}}}}')
    print(f'  ')
    print(f'  Login:    POST /api/v1/auth/login {{"username":"user","password":"pass123"}}')
    print(f'  Response: {{"token": "eyJ...", "user": {{...}}}}')
    print(f'  ')
    print(f'  Me:       GET  /api/v1/auth/me')
    print(f'  Headers:  Authorization: Bearer <token>')
    print(f'  ')
    print(f'  Logout:   POST /api/v1/auth/logout (remove token from client)')


def create_complete_auth():
    """Generate complete authentication with email verification"""
    print("\nGenerating complete authentication endpoints...")
    print("Endpoints: register, login, logout, verify-email, forgot-password, reset-password\n")

    # [1/3] Create complete auth controller
    print("[1/3] Creating complete auth controller...")
    controller_dir = Path("internal/controller")
    controller_dir.mkdir(parents=True, exist_ok=True)
    if not (controller_dir / "__init__.py").exists():
        (controller_dir / "__init__.py").write_text("", encoding="utf-8")

    controller_file = controller_dir / "auth_controller.py"
    controller_file.write_text(get_complete_auth_controller_template(), encoding="utf-8")

    # Update controller __init__.py
    controller_init_file = controller_dir / "__init__.py"
    controller_init_content = controller_init_file.read_text(encoding="utf-8")
    import_line = "from . import auth_controller"
    if import_line not in controller_init_content:
        controller_init_content += f"\n{import_line}\n"
        controller_init_file.write_text(controller_init_content, encoding="utf-8")

    # [2/3] Create complete auth routes
    print("[2/3] Creating complete auth routes...")
    routes_dir = Path("internal/routes")
    routes_dir.mkdir(parents=True, exist_ok=True)
    if not (routes_dir / "__init__.py").exists():
        (routes_dir / "__init__.py").write_text("", encoding="utf-8")

    route_file = routes_dir / "auth_route.py"
    route_file.write_text(get_complete_auth_route_template(), encoding="utf-8")

    # [3/3] Auto-register routes
    print("[3/3] Auto-registering routes...")
    register_auth_routes()

    print(f"\n✓ Complete authentication endpoints created successfully!")
    print(f"\nGenerated files:")
    print(f"  - internal/controller/auth_controller.py")
    print(f"  - internal/routes/auth_route.py")
    print(f"\nEndpoints:")
    print(f"  POST   /api/v1/auth/register         - Register new user (sends verification email)")
    print(f"  POST   /api/v1/auth/verify-email     - Verify email with code")
    print(f"  POST   /api/v1/auth/resend-verification - Resend verification email")
    print(f"  POST   /api/v1/auth/login            - Login user")
    print(f"  POST   /api/v1/auth/logout           - Logout user")
    print(f"  POST   /api/v1/auth/forgot-password  - Request password reset")
    print(f"  POST   /api/v1/auth/reset-password   - Reset password with code")
    print(f"  GET    /api/v1/auth/me               - Get current user info")
    print(f"\nEmail Configuration:")
    print(f"  Add to settings.py:")
    print(f"  EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development")
    print(f"  # For production, use SMTP:")
    print(f"  # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'")
    print(f"  # EMAIL_HOST = 'smtp.gmail.com'")
    print(f"  # EMAIL_PORT = 587")
    print(f"  # EMAIL_USE_TLS = True")
    print(f"  # EMAIL_HOST_USER = 'your-email@gmail.com'")
    print(f"  # EMAIL_HOST_PASSWORD = 'your-app-password'")


def register_auth_routes():
    """Auto-register auth routes in routes/__init__.py"""
    routes_init_file = Path("internal/routes/__init__.py")

    if routes_init_file.exists():
        routes_init_content = routes_init_file.read_text(encoding="utf-8")

        # Add import if not exists
        import_line = "from .auth_route import router as auth_router"
        if import_line not in routes_init_content:
            lines = routes_init_content.split("\n")
            insert_index = 0

            for i, line in enumerate(lines):
                if line.startswith("from .") and "_router" in line:
                    insert_index = i + 1

            if insert_index > 0 and lines[insert_index].strip():
                lines.insert(insert_index, "")
                insert_index += 1

            lines.insert(insert_index, import_line)
            routes_init_content = "\n".join(lines)

        # Update urlpatterns
        if "*auth_router" not in routes_init_content:
            if "urlpatterns = [" in routes_init_content:
                routes_init_content = routes_init_content.replace(
                    "urlpatterns = [", "urlpatterns = [*auth_router, ", 1
                )

        routes_init_file.write_text(routes_init_content, encoding="utf-8")
        print(f"  ✓ Updated internal/routes/__init__.py")
    else:
        print(f"  ✗ internal/routes/__init__.py not found")
