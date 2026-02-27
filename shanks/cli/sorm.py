"""SORM CLI - Database management commands"""

import subprocess
import sys
from pathlib import Path

from .banner import print_banner


def sorm_main():
    """SORM CLI entry point"""
    if len(sys.argv) < 2:
        print_banner()
        print("Database Manager\n")
        print("Usage:")
        print(
            "  sorm db push              Apply database changes (makemigrations + migrate)"
        )
        print("  sorm db pull              Show current database schema")
        print("  sorm db reset             Reset database (flush)")
        print("  sorm db seed              Run all seeders")
        print("  sorm makemigrations       Create new migrations")
        print("  sorm migrate              Apply migrations")
        print("  sorm showmigrations       Show migration status")
        sys.exit(1)

    command = sys.argv[1]

    if command == "db":
        if len(sys.argv) < 3:
            print("Usage: sorm db <push|pull|reset|seed>")
            sys.exit(1)

        subcommand = sys.argv[2]

        if subcommand == "push":
            # makemigrations + migrate
            print_banner()
            print("Pushing database changes...\n")
            print("Creating migrations...")
            result = subprocess.run(
                [sys.executable, "manage.py", "makemigrations"], check=False
            )
            if result.returncode != 0:
                sys.exit(1)

            print("\nApplying migrations...")
            result = subprocess.run(
                [sys.executable, "manage.py", "migrate"], check=False
            )
            if result.returncode != 0:
                sys.exit(1)

            print("\n✓ Database updated successfully!")

        elif subcommand == "pull":
            # Show current schema
            print_banner()
            print("Current database schema:\n")
            subprocess.run([sys.executable, "manage.py", "showmigrations"], check=True)

        elif subcommand == "reset":
            # Flush database
            print_banner()
            print("⚠️  This will delete all data from the database!\n")
            confirm = input("Are you sure? (yes/no): ")
            if confirm.lower() == "yes":
                subprocess.run(
                    [sys.executable, "manage.py", "flush", "--noinput"], check=True
                )
                print("\n✓ Database reset successfully!")
            else:
                print("Cancelled.")

        elif subcommand == "seed":
            # Run seeders
            print_banner()
            print("Running database seeders...\n")

            seeds_dir = Path("db/seeds")
            if not seeds_dir.exists():
                print("[ERROR] Seeds directory not found: db/seeds/")
                sys.exit(1)

            # Find all seed files
            seed_files = sorted(seeds_dir.glob("*_seed.py"))

            if not seed_files:
                print("[INFO] No seed files found in db/seeds/")
                print("Create seed files with pattern: {name}_seed.py")
                sys.exit(0)

            print(f"Found {len(seed_files)} seed file(s):\n")

            for seed_file in seed_files:
                seed_name = seed_file.stem.replace("_seed", "")
                print(f"[{seed_name}] Running...")

                # Execute seed file
                result = subprocess.run(
                    [
                        sys.executable,
                        "manage.py",
                        "shell",
                        "-c",
                        f"exec(open('{seed_file}').read())",
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    print(f"[{seed_name}] ✓ Success")
                else:
                    print(f"[{seed_name}] ✗ Failed")
                    if result.stderr:
                        print(f"  Error: {result.stderr}")

            print("\n✓ Seeding completed!")

        else:
            print(f"Unknown subcommand: {subcommand}")
            print("Available: push, pull, reset, seed")
            sys.exit(1)

    elif command == "makemigrations":
        # Pass through to Django
        subprocess.run(
            [sys.executable, "manage.py", "makemigrations"] + sys.argv[2:], check=True
        )

    elif command == "migrate":
        # Pass through to Django
        subprocess.run(
            [sys.executable, "manage.py", "migrate"] + sys.argv[2:], check=True
        )

    elif command == "showmigrations":
        # Pass through to Django
        subprocess.run(
            [sys.executable, "manage.py", "showmigrations"] + sys.argv[2:], check=True
        )

    else:
        print(f"Unknown command: {command}")
        print("\nAvailable commands:")
        print("  db              - Database operations (push, pull, reset, seed)")
        print("  makemigrations  - Create new migrations")
        print("  migrate         - Apply migrations")
        print("  showmigrations  - Show migration status")
        sys.exit(1)


if __name__ == "__main__":
    sorm_main()
