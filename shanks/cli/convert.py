"""Convert Shanks project to pure Django"""

import os
import shutil
import sys
from pathlib import Path

from .banner import print_banner


def generate_django():
    """Generate pure Django version in separate folder"""
    print_banner()
    print("Generating pure Django version...\n")
    
    # Check if we're in a Shanks project
    if not Path("manage.py").exists():
        print("[ERROR] Not in a Shanks project directory!")
        print("Run this command from your Shanks project root.")
        sys.exit(1)
    
    # Get project name from settings
    settings_files = list(Path(".").glob("*/settings.py"))
    if not settings_files:
        print("[ERROR] Could not find Django settings file!")
        sys.exit(1)
    
    project_name = settings_files[0].parent.name
    django_dir = Path(f"{project_name}-django")
    
    if django_dir.exists():
        print(f"[ERROR] Directory '{django_dir}' already exists!")
        confirm = input("Delete and recreate? (yes/no): ")
        if confirm.lower() != "yes":
            print("Cancelled.")
            sys.exit(1)
        shutil.rmtree(django_dir)
    
    print(f"[1/4] Creating Django project structure...")
    django_dir.mkdir()
    
    # Copy all files except venv and cache
    print(f"[2/4] Copying project files...")
    for item in Path(".").iterdir():
        if item.name in [".venv", "venv", "__pycache__", ".git", f"{project_name}-django"]:
            continue
        
        dest = django_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)
    
    print(f"[3/4] Converting Shanks code to Django...")
    
    # Convert routes to Django URLs
    routes_init = django_dir / "internal" / "routes" / "__init__.py"
    if routes_init.exists():
        content = routes_init.read_text(encoding="utf-8")
        
        # Add Django imports
        new_content = '''"""Django URL Configuration"""
from django.urls import path, re_path

# Import all route handlers
'''
        
        # Extract router imports and convert to Django paths
        lines = content.split('\n')
        for line in lines:
            if 'from .' in line and '_route import router' in line:
                # Extract module name
                module = line.split('from .')[1].split(' import')[0]
                new_content += f"from . import {module}\n"
        
        new_content += "\n# Django URL patterns\nurlpatterns = [\n"
        new_content += "    # Add your URL patterns here\n"
        new_content += "    # Example: path('api/health/', health_route.health, name='health'),\n"
        new_content += "]\n"
        
        routes_init.write_text(new_content, encoding="utf-8")
    
    # Update requirements.txt to remove shanks-django
    requirements = django_dir / "requirements.txt"
    if not requirements.exists():
        requirements.write_text("django>=3.2\n", encoding="utf-8")
    
    print(f"[4/4] Creating conversion guide...")
    
    guide = f"""# Django Conversion Guide

Your Shanks project has been converted to pure Django in: {django_dir}/

## What Changed

1. **Routes**: Shanks App routers need to be converted to Django URL patterns
   - Location: `internal/routes/__init__.py`
   - Convert `@router.get()` to `path()` or `re_path()`

2. **Controllers**: Already compatible with Django views
   - No changes needed

3. **Dependencies**: Remove `shanks-django` from requirements
   - Install: `pip install django`

## Next Steps

1. Review and update URL patterns in `internal/routes/__init__.py`
2. Update `requirements.txt` if needed
3. Test your application: `python manage.py runserver`

## Example Conversion

### Before (Shanks):
```python
@router.get('/api/posts')
def list_posts(req):
    return posts_controller.list(req)
```

### After (Django):
```python
urlpatterns = [
    path('api/posts/', posts_route.list_posts, name='list_posts'),
]
```

## Need Help?

- Django URLs: https://docs.djangoproject.com/en/stable/topics/http/urls/
- Django Views: https://docs.djangoproject.com/en/stable/topics/http/views/
"""
    
    (django_dir / "CONVERSION_GUIDE.md").write_text(guide, encoding="utf-8")
    
    print(f"\n✓ Django version generated successfully!")
    print(f"\nLocation: {django_dir}/")
    print(f"Guide: {django_dir}/CONVERSION_GUIDE.md")
    print(f"\nNext steps:")
    print(f"  cd {django_dir}")
    print(f"  # Review CONVERSION_GUIDE.md")
    print(f"  # Update URL patterns")
    print(f"  python manage.py runserver")


def kamusari():
    """Convert Shanks project to Django in-place (destructive)"""
    print_banner()
    print("⚠️  KAMUSARI - In-place Django Conversion\n")
    print("WARNING: This will REPLACE all Shanks code with pure Django!")
    print("This operation is DESTRUCTIVE and cannot be undone.")
    print("\nRecommendation: Use 'shanks generate django' instead for a safe conversion.\n")
    
    confirm1 = input("Are you sure you want to continue? (yes/no): ")
    if confirm1.lower() != "yes":
        print("Cancelled.")
        sys.exit(0)
    
    confirm2 = input("Type 'KAMUSARI' to confirm: ")
    if confirm2 != "KAMUSARI":
        print("Cancelled.")
        sys.exit(0)
    
    print("\n[1/3] Backing up project...")
    backup_dir = Path("shanks-backup")
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    
    # Create backup
    backup_dir.mkdir()
    for item in Path(".").iterdir():
        if item.name in [".venv", "venv", "__pycache__", ".git", "shanks-backup"]:
            continue
        
        dest = backup_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)
    
    print(f"[2/3] Converting to Django...")
    
    # Convert routes
    routes_init = Path("internal/routes/__init__.py")
    if routes_init.exists():
        content = routes_init.read_text(encoding="utf-8")
        
        new_content = '''"""Django URL Configuration"""
from django.urls import path, re_path

# Import all route handlers
'''
        
        lines = content.split('\n')
        for line in lines:
            if 'from .' in line and '_route import router' in line:
                module = line.split('from .')[1].split(' import')[0]
                new_content += f"from . import {module}\n"
        
        new_content += "\n# Django URL patterns\nurlpatterns = [\n"
        new_content += "    # Add your URL patterns here\n"
        new_content += "]\n"
        
        routes_init.write_text(new_content, encoding="utf-8")
    
    # Update requirements
    requirements = Path("requirements.txt")
    if requirements.exists():
        content = requirements.read_text(encoding="utf-8")
        content = content.replace("shanks-django", "# shanks-django (removed)")
        requirements.write_text(content, encoding="utf-8")
    
    print(f"[3/3] Creating conversion notes...")
    
    notes = """# KAMUSARI Conversion Complete

Your project has been converted to pure Django IN-PLACE.

## Backup

A backup of your original Shanks project is in: shanks-backup/

## What Changed

1. Routes converted to Django URL patterns
2. shanks-django removed from requirements
3. You need to manually update URL patterns

## Next Steps

1. Review internal/routes/__init__.py
2. Convert all Shanks routes to Django URL patterns
3. Test: python manage.py runserver

## Restore Backup

If you need to restore:
  rm -rf internal/ entity/ dto/
  cp -r shanks-backup/* .
"""
    
    Path("KAMUSARI_NOTES.md").write_text(notes, encoding="utf-8")
    
    print(f"\n✓ Conversion complete!")
    print(f"\nBackup: shanks-backup/")
    print(f"Notes: KAMUSARI_NOTES.md")
    print(f"\n⚠️  Remember to update your URL patterns!")
