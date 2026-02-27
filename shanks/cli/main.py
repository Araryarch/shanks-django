"""Main CLI entry point"""

import sys

from .commands import create_project, run_server
from .crud import create_crud_endpoint
from .convert import generate_django, kamusari


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("Shanks CLI")
        print("\nUsage:")
        print("  shanks new <project_name>        Create new project")
        print("  shanks run                       Start development server")
        print("  shanks create <name> --crud      Generate CRUD endpoint")
        print("  shanks generate django           Convert to pure Django (safe)")
        print(
            "  shanks kamusari                  Convert to Django in-place (destructive)"
        )
        sys.exit(1)

    command = sys.argv[1]

    if command == "new":
        create_project()
    elif command == "run":
        run_server()
    elif command == "create":
        create_crud_endpoint()
    elif command == "generate":
        if len(sys.argv) < 3 or sys.argv[2] != "django":
            print("Usage: shanks generate django")
            sys.exit(1)
        generate_django()
    elif command == "kamusari":
        kamusari()
    else:
        print(f"Unknown command: {command}")
        print("\nAvailable commands:")
        print("  new             - Create new project")
        print("  run             - Start development server")
        print("  create          - Generate CRUD endpoint")
        print("  generate django - Convert to pure Django (safe)")
        print("  kamusari        - Convert to Django in-place (destructive)")
        sys.exit(1)


if __name__ == "__main__":
    main()
