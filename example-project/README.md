# Shanks Django Example Project

Express.js-like API built with Shanks Django framework.

## Features

- ✨ **No urls.py needed** - routes auto-configured
- 🚀 Simple routing with grouping (like Gin/Express)
- 🔐 JWT Authentication
- 📝 Blog API (Posts, Comments, Categories, Tags)
- 🎨 Auto-generated Swagger UI
- 🔄 CORS enabled
- 📦 SQLite database (easily switch to PostgreSQL/MySQL)
- ⚡ Prisma-like ORM syntax

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
shanks run
# or
python manage.py runserver
```

Visit:
- API: http://127.0.0.1:8000/api/health
- Swagger: http://127.0.0.1:8000/swagger

## Project Structure

```
example-project/
├── settings.py          # Super simple config with Shanks helpers
├── wsgi.py             # Minimal WSGI config
├── manage.py           # Django management
└── app/
    ├── routes/
    │   ├── __init__.py  # Main routes - exports urlpatterns
    │   ├── auth.py      # Authentication routes
    │   ├── posts.py     # Post routes
    │   ├── comments.py  # Comment routes
    │   └── ...
    ├── models/          # Database models
    ├── dto/            # Data Transfer Objects
    ├── middleware/     # Custom middleware
    └── utils/          # Utilities
```

## Settings Configuration

Shanks provides built-in helpers for super simple settings:

```python
# settings.py
from shanks import (
    get_base_dir,
    get_secret_key,
    get_debug,
    get_allowed_hosts,
    get_database,
    get_installed_apps,
    get_middleware,
    get_templates,
    get_password_validators,
)

# Paths
BASE_DIR = get_base_dir(__file__)

# Security (auto-loads from .env)
SECRET_KEY = get_secret_key()
DEBUG = get_debug()
ALLOWED_HOSTS = get_allowed_hosts()

# Apps
INSTALLED_APPS = get_installed_apps(["app"])

# Middleware
MIDDLEWARE = get_middleware()

# Routing
ROOT_URLCONF = "app.routes"

# Templates
TEMPLATES = get_templates()

# WSGI
WSGI_APPLICATION = "wsgi.application"

# Database (auto-loads from DATABASE_URL env var)
DATABASES = get_database(BASE_DIR)

# Password validation (disabled in DEBUG mode)
AUTH_PASSWORD_VALIDATORS = get_password_validators(DEBUG)

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

**That's it! No manual dotenv loading, no complex configuration.**

## WSGI Configuration

Minimal WSGI config:

```python
# wsgi.py
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Routing Example

```python
# app/routes/__init__.py
from shanks import App
from . import auth, posts, comments

app = App()

# Include all routers - Simple!
app.include(auth.router, posts.router, comments.router)

# Export urlpatterns - No urls.py needed!
urlpatterns = app.get_urls()
```

```python
# app/routes/posts.py
from shanks import App

router = App()

@router.get("api/posts")
def list_posts(req):
    return {"posts": []}

@router.post("api/posts")
def create_post(req):
    return {"post": {}}
```

**That's it! No Django urls.py complexity.**

## API Endpoints

### Authentication
- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login
- GET `/api/auth/me` - Get current user

### Posts
- GET `/api/posts` - List posts
- POST `/api/posts` - Create post
- GET `/api/posts/:id` - Get post
- PUT `/api/posts/:id` - Update post
- DELETE `/api/posts/:id` - Delete post
- POST `/api/posts/:id/like` - Like/unlike post

### Comments
- POST `/api/posts/:id/comments` - Add comment

### Categories & Tags
- GET `/api/categories` - List categories
- GET `/api/tags` - List tags

See full API documentation at `/swagger`

## Environment Variables

```bash
# .env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=sqlite:///db.sqlite3  # or postgres://...
JWT_SECRET=your-jwt-secret
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Prisma-like ORM

```python
from shanks import User, Post

# Find
users = User.find_many()
user = User.find_unique(username='john')

# Create
user = User.create(username='john', email='john@example.com')

# Update
user.update_self(email='new@example.com')

# Delete
user.delete_self()

# Count
total = User.count()
```

## Testing with Bruno

API tests are available in the `bruno/` directory. Install [Bruno](https://www.usebruno.com/) and open the collection.

## Learn More

- [Routing Examples](ROUTING_EXAMPLE.md) - Learn about route grouping
- [Quick Start Guide](QUICKSTART.md) - Step-by-step tutorial
- [Shanks Documentation](../README.md) - Full framework docs
