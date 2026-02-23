# Quick Start Guide

## 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## 2. Run Server

```bash
# Using Shanks CLI (with auto-reload)
shanks run

# Or using Django
python manage.py runserver
```

## 3. Access

- API: http://localhost:8000/api/
- Swagger Docs: http://localhost:8000/docs
- Admin Panel: http://localhost:8000/admin

## 4. Test API

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "password123"
  }'
```

### Create Post (with token)
```bash
curl -X POST http://localhost:8000/api/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first post",
    "excerpt": "A short excerpt"
  }'
```

### Get Posts
```bash
curl http://localhost:8000/api/posts
```

### Create Comment
```bash
curl -X POST http://localhost:8000/api/posts/1/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "content": "Great post!"
  }'
```

## 5. Frontend Integration

### React Example

```javascript
// Login
const login = async (username, password) => {
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await response.json();
  localStorage.setItem('token', data.token);
  return data;
};

// Get Posts
const getPosts = async () => {
  const response = await fetch('http://localhost:8000/api/posts');
  return response.json();
};

// Create Post
const createPost = async (title, content) => {
  const token = localStorage.getItem('token');
  const response = await fetch('http://localhost:8000/api/posts', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ title, content })
  });
  return response.json();
};
```

## 6. Project Structure

```
example-project/
├── app/
│   ├── config.py           # Configuration
│   ├── dto/                # Data Transfer Objects
│   ├── middleware/         # Middleware (auth, logger)
│   ├── models/             # Django Models
│   ├── routes/             # API Routes
│   └── utils/              # Utilities (JWT, validators)
├── manage.py
├── settings.py
├── urls.py
└── requirements.txt
```

## 7. Available Endpoints

### Authentication
- POST `/api/auth/register` - Register
- POST `/api/auth/login` - Login
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
- POST `/api/posts/<id>/like` - Like/Unlike post

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
- DELETE `/api/tags/<id>` - Delete tag
