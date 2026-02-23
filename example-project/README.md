# Blog API - Shanks Django Example Project

Complete example project with authentication and CRUD operations using Shanks Django framework with Prisma-like ORM.

## Features

- 🔐 JWT Authentication
- 👤 User Management
- 📝 Blog Posts CRUD
- 💬 Comments CRUD
- 🏷️ Categories CRUD
- 🔖 Tags CRUD
- 👍 Likes System
- 📚 Swagger Documentation
- 🌐 CORS Enabled
- 🗄️ PostgreSQL/SQLite Support
- ⚡ Prisma-like ORM Syntax
- 🎯 Express.js-like Routes
- 🚀 Clean Architecture

## What's Special

This example project demonstrates:
- **No Django imports in routes** - Everything wrapped in Shanks
- **Prisma-like ORM** - `find_many()`, `find_unique()`, `create()`, etc.
- **Express.js syntax** - `@app.get()`, `@app.post()`, etc.
- **Clean architecture** - DTOs, middleware, services separation
- **Modern patterns** - JWT auth, validation, error handling

## Architecture

```
example-project/
├── app/
│   ├── __init__.py
│   ├── config.py           # Configuration
│   ├── middleware/         # Middleware
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── logger.py
│   ├── dto/                # Data Transfer Objects
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── models/             # Django Models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   ├── category.py
│   │   └── tag.py
│   ├── routes/             # API Routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── posts.py
│   │   ├── comments.py
│   │   ├── categories.py
│   │   └── tags.py
│   ├── services/           # Business Logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── post_service.py
│   └── utils/              # Utilities
│       ├── __init__.py
│       ├── jwt.py
│       └── validators.py
├── manage.py
├── requirements.txt
└── README.md
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create superuser:
```bash
python manage.py createsuperuser
```

4. Run server:
```bash
shanks run
# or
python manage.py runserver
```

5. Visit:
- API: http://localhost:8000/api/
- Swagger: http://localhost:8000/docs
- Admin: http://localhost:8000/admin

## API Endpoints

### Authentication
- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login
- POST `/api/auth/logout` - Logout
- GET `/api/auth/me` - Get current user

### Users
- GET `/api/users` - List users
- GET `/api/users/<id>` - Get user
- PUT `/api/users/<id>` - Update user
- DELETE `/api/users/<id>` - Delete user

### Posts
- GET `/api/posts` - List posts
- POST `/api/posts` - Create post
- GET `/api/posts/<id>` - Get post
- PUT `/api/posts/<id>` - Update post
- DELETE `/api/posts/<id>` - Delete post
- POST `/api/posts/<id>/like` - Like post

### Comments
- GET `/api/posts/<post_id>/comments` - List comments
- POST `/api/posts/<post_id>/comments` - Create comment
- PUT `/api/comments/<id>` - Update comment
- DELETE `/api/comments/<id>` - Delete comment

### Categories
- GET `/api/categories` - List categories
- POST `/api/categories` - Create category
- GET `/api/categories/<id>` - Get category
- PUT `/api/categories/<id>` - Update category
- DELETE `/api/categories/<id>` - Delete category

### Tags
- GET `/api/tags` - List tags
- POST `/api/tags` - Create tag
- GET `/api/tags/<id>` - Get tag
- PUT `/api/tags/<id>` - Update tag
- DELETE `/api/tags/<id>` - Delete tag

## Testing

```bash
pytest
```

## Code Examples

### Prisma-like ORM Usage

```python
from shanks import User, Model, CharField, TextField

# Find users
users = User.find_many()
user = User.find_unique(username='john')
active_users = User.find_many(is_active=True)

# Create user
user = User.create(
    username='john',
    email='john@example.com',
    password='secret123'
)

# Update user
user.update_self(email='newemail@example.com')

# Delete user
user.delete_self()

# Count
total = User.count()
active_count = User.count(is_active=True)
```

### Express.js-like Routes

```python
from shanks import App, Response

app = App()

@app.get('api/posts')
def list_posts(req):
    posts = Post.find_many()
    return {'posts': [{'id': p.id, 'title': p.title} for p in posts]}

@app.post('api/posts')
def create_post(req):
    post = Post.create(
        title=req.body.get('title'),
        content=req.body.get('content'),
        author=req.user
    )
    return Response().status_code(201).json({'id': post.id})
```

### No Django Imports

All Django functionality is wrapped in Shanks:

```python
# ❌ Old way (Django)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.text import slugify

# ✅ New way (Shanks)
from shanks import User, authenticate, slugify
```

## Learn More

See the main [Shanks Django README](../README.md) for complete documentation.
