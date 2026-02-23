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
├── settings.py          # Django settings (minimal config)
├── wsgi.py             # WSGI (auto-configured by Shanks)
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
