# Blog API - Shanks Django Example Project

Complete example project with authentication and CRUD operations.

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
