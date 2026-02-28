"""
Example seed file
Run with: sorm db seed
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalapp.settings')
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
