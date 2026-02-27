"""Main CLI entry point"""

import sys

from .commands import create_project, run_server
from .crud import create_crud_endpoint


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("Shanks CLI")
        print("\nUsage:")
        print("  shanks new <project_name>        Create new project")
        print("  shanks run                       Start development server")
        print("  shanks create <name> --crud      Generate CRUD endpoint")
        sys.exit(1)

    command = sys.argv[1]

    if command == "new":
        create_project()
    elif command == "run":
        run_server()
    elif command == "create":
        create_crud_endpoint()
    else:
        print(f"Unknown command: {command}")
        print("\nAvailable commands:")
        print("  new     - Create new project")
        print("  run     - Start development server")
        print("  create  - Generate CRUD endpoint")
        sys.exit(1)


if __name__ == "__main__":
    main()
