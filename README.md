![shanks](https://github.com/user-attachments/assets/70a7c689-f475-41b4-862b-6b9371d127e9)

# Shanks Django

🚀 Express.js-like framework built on Django. Write Django APIs with Express.js syntax and Prisma-like ORM.

[![PyPI version](https://badge.fury.io/py/shanks-django.svg)](https://pypi.org/project/shanks-django/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🎯 **Express.js-like syntax** - Familiar routing for Node.js developers
- 🔥 **Prisma-like ORM** - Modern database queries with `find_many()`, `create()`, etc.
- 🚀 **Built on Django** - Full Django power under the hood
- 🔧 **Middleware support** - Express-style middleware
- 📦 **Simple Request/Response** - Clean API for handling HTTP
- 🎨 **Built-in formatter** - Black code formatting
- 🔍 **Built-in linter** - Flake8 linting
- ⚡ **Auto-reload dev server** - Like nodemon for Python
- 🗄️ **Multi-database support** - PostgreSQL, MySQL, MongoDB, Redis
- 📚 **Swagger/OpenAPI** - Auto-generated API documentation
- 🌐 **CORS built-in** - Easy cross-origin setup
- 🎁 **VSCode Extension** - Snippets and IntelliSense

## 📦 Installation

```bash
pip install shanks-django
```

### With Database Support

```bash
# PostgreSQL
pip install shanks-django[postgres]

# MySQL
pip install shanks-django[mysql]

# MongoDB
pip install shanks-django[mongodb]

# Redis
pip install shanks-django[redis]

# All databases
pip install shanks-django[all]
```

## 🚀 Quick Start

### Option 1: Auto-generate Project

```bash
shanks new myproject
cd myproject
shanks run
```

### Option 2: Manual Setup

1. Install dependencies:
```bash
pip install shanks-django django
```

2. Create Django project:
```bash
django-admin startproject myproject
cd myproject
```

3. Create `app/routes/__init__.py`:
```python
from shanks import App

app = App()

@app.get('api/hello')
def hello(req):
    return {'message': 'Hello from Shanks!'}

# Export URL patterns - no urls.py needed!
urlpatterns = app.get_urls()
```

4. Update `settings.py`:
```python
from shanks import (
    get_base_dir, get_secret_key, get_debug,
    get_allowed_hosts, get_database, get_installed_apps,
    get_middleware, get_templates
)

BASE_DIR = get_base_dir(__file__)
SECRET_KEY = get_secret_key()
DEBUG = get_debug()
ALLOWED_HOSTS = get_allowed_hosts()

INSTALLED_APPS = get_installed_apps(['app'])
MIDDLEWARE = get_middleware()
ROOT_URLCONF = 'app.routes'  # Point directly to routes!
TEMPLATES = get_templates()
WSGI_APPLICATION = 'wsgi.application'
DATABASES = get_database(BASE_DIR)

# ... rest of settings
```

5. Create minimal `wsgi.py`:
```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
application = get_wsgi_application()
```

6. Run server:
```bash
shanks run
# Visit: http://127.0.0.1:8000/api/hello
```

## 🛠️ CLI Commands

```bash
# Development server with auto-reload (like nodemon)
shanks run                    # Start on 127.0.0.1:8000
shanks run 3000               # Start on port 3000
shanks run 0.0.0.0:8000       # Start on all interfaces

# Project management
shanks new myproject          # Create new project

# Code quality
shanks format                 # Format with Black
shanks lint                   # Lint with Flake8
shanks check                  # Format + Lint

# Database migrations
shanks migrate                # Run migrations
shanks makemigrations         # Create migrations
shanks push                   # Create and run migrations (Prisma-like)

# Help
shanks help                   # Show all commands
```

## 📖 Core Concepts

### 1. Routes (Express.js-like)

```python
from shanks import App

app = App()

# GET route
@app.get('api/users')
def get_users(req):
    return {'users': []}

# POST route
@app.post('api/users')
def create_user(req):
    data = req.body
    return {'created': True, 'data': data}

# PUT route
@app.put('api/users/<int:user_id>')
def update_user(req, user_id):
    return {'updated': True, 'id': user_id}

# DELETE route
@app.delete('api/users/<int:user_id>')
def delete_user(req, user_id):
    return {'deleted': True, 'id': user_id}

# PATCH route
@app.patch('api/users/<int:user_id>')
def patch_user(req, user_id):
    return {'patched': True}

urlpatterns = app.get_urls()
```

### 2. Request Object

```python
@app.post('api/data')
def handle_data(req):
    # Get JSON body
    data = req.body
    name = req.body.get('name')
    
    # Get query parameters
    page = req.query.get('page', 1)
    limit = req.query.get('limit', 10)
    
    # Get headers
    auth = req.headers.get('Authorization')
    content_type = req.headers.get('Content-Type')
    
    # Get cookies
    token = req.cookies.get('token')
    
    # Get uploaded files
    file = req.files.get('file')
    
    # Get authenticated user (Django)
    user = req.user
    is_authenticated = req.user.is_authenticated
    
    # Get session (Django)
    cart = req.session.get('cart', [])
    req.session['key'] = 'value'
    
    # HTTP method and path
    method = req.method  # GET, POST, etc.
    path = req.path      # /api/data
    
    # Access full Django request
    django_req = req.django
    
    return {'status': 'ok'}
```

### 3. Response Object

```python
from shanks import App, Response

app = App()

# Simple JSON response
@app.get('api/data')
def get_data(req):
    return {'data': 'value'}  # Auto-converts to JSON

# Using Response object
@app.get('api/custom')
def custom(req):
    return Response().json({'data': 'value'})

# Custom status code
@app.post('api/create')
def create(req):
    return Response().status_code(201).json({'created': True})

# Set headers
@app.get('api/headers')
def with_headers(req):
    return (Response()
        .header('X-Custom-Header', 'value')
        .header('X-Another', 'value2')
        .json({'ok': True}))

# Set cookies
@app.post('api/login')
def login(req):
    return (Response()
        .cookie('token', 'abc123', max_age=3600)
        .cookie('refresh', 'xyz789', max_age=86400)
        .json({'logged_in': True}))

# Redirect
@app.get('old-url')
def old_url(req):
    return Response().redirect('/new-url')

# Render Django template
@app.get('dashboard')
def dashboard(req):
    context = {'title': 'Dashboard', 'user': req.user}
    return Response().render(req.django, 'dashboard.html', context)

# File download
@app.get('api/download')
def download(req):
    return Response().file('/path/to/file.pdf', 'document.pdf')
```

### 4. Middleware (Express.js-like)

```python
from shanks import App, Response

app = App()

# Simple logging middleware
def logger(req):
    print(f"{req.method} {req.path}")

app.use(logger)

# Auth middleware
def auth_middleware(req):
    token = req.headers.get('Authorization')
    if not token:
        return Response().status_code(401).json({'error': 'Unauthorized'})
    # If returns None, continues to next middleware/route

app.use(auth_middleware)

# CORS middleware
def cors_middleware(req):
    # Add CORS headers to response
    pass

app.use(cors_middleware)

# Multiple middleware
app.use(logger)
app.use(auth_middleware)
app.use(cors_middleware)

@app.get('api/protected')
def protected(req):
    return {'data': 'secret'}
```

## 🗄️ Prisma-like ORM

Shanks provides a modern, Prisma-inspired ORM syntax on top of Django ORM.

### Define Models

```python
from shanks import Model, CharField, TextField, DateTimeField, ForeignKey, CASCADE

class Post(Model):
    title = CharField(max_length=200)
    content = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
```

### Available Field Types

```python
from shanks import (
    CharField,          # String field
    TextField,          # Long text
    IntegerField,       # Integer
    FloatField,         # Float
    BooleanField,       # Boolean
    DateField,          # Date
    DateTimeField,      # DateTime
    EmailField,         # Email
    URLField,           # URL
    SlugField,          # Slug
    JSONField,          # JSON data
    
    # Relationships
    ForeignKey,         # One-to-many
    ManyToManyField,    # Many-to-many
    OneToOneField,      # One-to-one
    
    # Relationship options
    CASCADE,            # Delete related
    SET_NULL,           # Set to NULL
    PROTECT,            # Prevent deletion
)
```

### Query Methods (Prisma-like)

```python
from app.models import Post

# Find many records
posts = Post.find_many()
posts = Post.find_many(author=user)
posts = Post.find_many(title__contains='Django')

# Find first record
post = Post.find_first(slug='hello-world')
post = Post.find_first(author=user, published=True)

# Find unique record (returns None if not found)
post = Post.find_unique(id=1)
post = Post.find_unique(slug='hello-world')

# Create record
post = Post.create(
    title='Hello World',
    content='This is my first post',
    author=user
)

# Update records
Post.update(
    where={'author': user},
    data={'published': True}
)

# Delete many records
Post.delete_many(published=False)
Post.delete_many(created_at__lt=old_date)

# Count records
total = Post.count()
published_count = Post.count(published=True)

# Update instance
post = Post.find_unique(id=1)
post.update_self(title='New Title', content='New content')

# Delete instance
post = Post.find_unique(id=1)
post.delete_self()
```

### User Model (Built-in)

```python
from shanks import User, authenticate

# Find users
users = User.find_many()
user = User.find_unique(username='john')
user = User.find_first(email='john@example.com')

# Create user
user = User.create(
    username='john',
    email='john@example.com',
    password='secret123',  # Auto-hashed
    first_name='John',
    last_name='Doe'
)

# Authenticate user
user = authenticate(username='john', password='secret123')
if user:
    print('Login successful')

# Update user
user.update_self(
    first_name='Johnny',
    email='johnny@example.com'
)

# Update password
user.update_self(password='newpassword')  # Auto-hashed

# Count users
total_users = User.count()
active_users = User.count(is_active=True)
```

### Complete CRUD Example

```python
from shanks import App, Response, Model, CharField, TextField, ForeignKey, CASCADE, User
from shanks import slugify

# Define Model
class Post(Model):
    title = CharField(max_length=200)
    slug = CharField(max_length=200, unique=True)
    content = TextField()
    author = ForeignKey(User, on_delete=CASCADE, related_name='posts')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

# Routes
app = App()

# List all posts
@app.get('api/posts')
def list_posts(req):
    posts = Post.find_many()
    return {
        'posts': [{
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'author': p.author.username
        } for p in posts]
    }

# Get single post
@app.get('api/posts/<int:post_id>')
def get_post(req, post_id):
    post = Post.find_unique(id=post_id)
    if not post:
        return Response().status_code(404).json({'error': 'Post not found'})
    
    return {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username
    }

# Create post
@app.post('api/posts')
def create_post(req):
    post = Post.create(
        title=req.body.get('title'),
        content=req.body.get('content'),
        author=req.user
    )
    return Response().status_code(201).json({'id': post.id})

# Update post
@app.put('api/posts/<int:post_id>')
def update_post(req, post_id):
    post = Post.find_unique(id=post_id)
    if not post:
        return Response().status_code(404).json({'error': 'Not found'})
    
    post.update_self(
        title=req.body.get('title'),
        content=req.body.get('content')
    )
    return {'updated': True}

# Delete post
@app.delete('api/posts/<int:post_id>')
def delete_post(req, post_id):
    post = Post.find_unique(id=post_id)
    if not post:
        return Response().status_code(404).json({'error': 'Not found'})
    
    post.delete_self()
    return {'deleted': True}

urlpatterns = app.get_urls()
```

## 🌐 CORS Support

```python
from shanks import App, CORS

app = App()

# Enable CORS for all origins (development)
CORS.enable(app)

# Production: Specific origins
CORS.enable(app,
    origins=['https://myapp.com', 'https://www.myapp.com'],
    methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
    headers=['Content-Type', 'Authorization', 'X-Custom-Header'],
    credentials=True,  # Allow cookies
    max_age=3600       # Cache preflight for 1 hour
)

# Multiple origins
CORS.enable(app,
    origins=[
        'http://localhost:3000',      # React dev
        'http://localhost:5173',      # Vite dev
        'https://myapp.com',          # Production
    ],
    credentials=True
)

@app.get('api/data')
def get_data(req):
    return {'data': 'value'}
```

## 📚 Swagger/OpenAPI Documentation

```python
from shanks import App, SwaggerUI

app = App()

# Enable Swagger UI at /docs
SwaggerUI.enable(app,
    title="My API",
    version="1.0.0",
    description="Complete API documentation"
)

# Document routes
@app.get('api/users/<int:user_id>')
@SwaggerUI.doc(
    summary="Get user by ID",
    description="Returns a single user with all details",
    tags=["Users"],
    parameters=[{
        "name": "user_id",
        "in": "path",
        "required": True,
        "schema": {"type": "integer"},
        "description": "User ID"
    }],
    responses={
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "username": {"type": "string"},
                            "email": {"type": "string"}
                        }
                    }
                }
            }
        },
        404: {"description": "User not found"}
    }
)
def get_user(req, user_id):
    user = User.find_unique(id=user_id)
    if not user:
        return Response().status_code(404).json({'error': 'Not found'})
    return {'id': user.id, 'username': user.username, 'email': user.email}

# Document POST with request body
@app.post('api/users')
@SwaggerUI.doc(
    summary="Create user",
    tags=["Users"],
    request_body={
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["username", "email", "password"],
                    "properties": {
                        "username": {"type": "string"},
                        "email": {"type": "string", "format": "email"},
                        "password": {"type": "string", "minLength": 8}
                    }
                }
            }
        }
    }
)
def create_user(req):
    user = User.create(
        username=req.body.get('username'),
        email=req.body.get('email'),
        password=req.body.get('password')
    )
    return Response().status_code(201).json({'id': user.id})

# Visit: http://localhost:8000/docs
```

## 🗄️ Database Support

### PostgreSQL

```python
# settings.py
from shanks import DatabaseConfig

DATABASES = {
    'default': DatabaseConfig.postgres(
        host='localhost',
        port=5432,
        database='mydb',
        user='postgres',
        password='password'
    )
}

# Or from environment variable
import os
DATABASES = {
    'default': DatabaseConfig.from_url(os.getenv('DATABASE_URL'))
}
# DATABASE_URL format: postgresql://user:pass@host:port/dbname
```

### MySQL

```python
# settings.py
from shanks import DatabaseConfig

DATABASES = {
    'default': DatabaseConfig.mysql(
        host='localhost',
        port=3306,
        database='mydb',
        user='root',
        password='password'
    )
}
```

### SQLite

```python
# settings.py
from shanks import DatabaseConfig

DATABASES = {
    'default': DatabaseConfig.sqlite('db.sqlite3')
}
```

### MongoDB

```python
from shanks import MongoDB, App

# Connect to MongoDB
MongoDB.connect(
    host='localhost',
    port=27017,
    database='mydb',
    username='user',
    password='pass'
)

app = App()

# Use MongoDB
@app.get('api/products')
def get_products(req):
    products = list(MongoDB.db.products.find({}, {'_id': 0}))
    return {'products': products}

@app.post('api/products')
def create_product(req):
    product = {
        'name': req.body.get('name'),
        'price': req.body.get('price'),
        'stock': req.body.get('stock')
    }
    result = MongoDB.db.products.insert_one(product)
    return {'id': str(result.inserted_id)}

@app.get('api/products/<product_id>')
def get_product(req, product_id):
    from bson import ObjectId
    product = MongoDB.db.products.find_one({'_id': ObjectId(product_id)})
    if product:
        product['_id'] = str(product['_id'])
        return product
    return Response().status_code(404).json({'error': 'Not found'})
```

### Redis

```python
from shanks import Redis, App

# Connect to Redis
Redis.connect(
    host='localhost',
    port=6379,
    password='password',
    db=0
)

app = App()

# Cache example
@app.get('api/cache/<key>')
def get_cache(req, key):
    value = Redis.client.get(key)
    if value:
        return {'key': key, 'value': value.decode()}
    return Response().status_code(404).json({'error': 'Not found'})

@app.post('api/cache')
def set_cache(req):
    key = req.body.get('key')
    value = req.body.get('value')
    ttl = req.body.get('ttl', 3600)  # 1 hour default
    
    Redis.client.setex(key, ttl, value)
    return {'success': True, 'expires_in': ttl}

@app.delete('api/cache/<key>')
def delete_cache(req, key):
    Redis.client.delete(key)
    return {'deleted': True}
```

### Multi-Database Example

```python
from shanks import App, Model, CharField, ForeignKey, CASCADE, User
from shanks import MongoDB, Redis

# PostgreSQL Model (Django ORM)
class Product(Model):
    name = CharField(max_length=200)
    price = IntegerField()
    stock = IntegerField()

app = App()

@app.post('api/orders')
def create_order(req):
    # Get product from PostgreSQL
    product = Product.find_unique(id=req.body.get('product_id'))
    if not product:
        return Response().status_code(404).json({'error': 'Product not found'})
    
    # Check cache in Redis
    cache_key = f'stock:{product.id}'
    cached_stock = Redis.client.get(cache_key)
    
    # Create order in MongoDB
    order = {
        'user_id': req.user.id,
        'product_id': product.id,
        'product_name': product.name,
        'price': product.price,
        'quantity': req.body.get('quantity'),
        'status': 'pending'
    }
    result = MongoDB.db.orders.insert_one(order)
    
    # Update stock in PostgreSQL
    product.update_self(stock=product.stock - order['quantity'])
    
    # Update cache in Redis
    Redis.client.setex(cache_key, 3600, product.stock)
    
    return {'order_id': str(result.inserted_id)}
```

## 🔐 Authentication & Authorization

### JWT Authentication Example

```python
from shanks import App, Response, User, authenticate
import jwt
from datetime import datetime, timedelta

app = App()

SECRET_KEY = 'your-secret-key'

def create_token(user_id, username):
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Auth middleware
def auth_required(req):
    auth_header = req.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response().status_code(401).json({'error': 'Unauthorized'})
    
    token = auth_header.split(' ')[1]
    payload = verify_token(token)
    if not payload:
        return Response().status_code(401).json({'error': 'Invalid token'})
    
    # Attach user to request
    req.user = User.find_unique(id=payload['user_id'])
    if not req.user:
        return Response().status_code(401).json({'error': 'User not found'})

# Register
@app.post('api/auth/register')
def register(req):
    username = req.body.get('username')
    email = req.body.get('email')
    password = req.body.get('password')
    
    if User.find_unique(username=username):
        return Response().status_code(400).json({'error': 'Username exists'})
    
    user = User.create(username=username, email=email, password=password)
    token = create_token(user.id, user.username)
    
    return Response().status_code(201).json({
        'token': token,
        'user': {'id': user.id, 'username': user.username, 'email': user.email}
    })

# Login
@app.post('api/auth/login')
def login(req):
    username = req.body.get('username')
    password = req.body.get('password')
    
    user = authenticate(username=username, password=password)
    if not user:
        return Response().status_code(401).json({'error': 'Invalid credentials'})
    
    token = create_token(user.id, user.username)
    return {'token': token, 'user': {'id': user.id, 'username': user.username}}

# Protected route
@app.get('api/auth/me')
def get_me(req):
    auth_response = auth_required(req)
    if auth_response:
        return auth_response
    
    return {
        'id': req.user.id,
        'username': req.user.username,
        'email': req.user.email
    }
```

## 🎯 Advanced Features

### URL Parameters

```python
# Path parameters
@app.get('api/users/<int:user_id>')
def get_user(req, user_id):
    return {'id': user_id}

@app.get('api/posts/<slug:slug>')
def get_post(req, slug):
    return {'slug': slug}

@app.get('api/files/<path:filepath>')
def get_file(req, filepath):
    return {'path': filepath}

# Multiple parameters
@app.get('api/users/<int:user_id>/posts/<int:post_id>')
def get_user_post(req, user_id, post_id):
    return {'user_id': user_id, 'post_id': post_id}

# Query parameters
@app.get('api/search')
def search(req):
    query = req.query.get('q')
    page = int(req.query.get('page', 1))
    limit = int(req.query.get('limit', 10))
    
    # /api/search?q=django&page=2&limit=20
    return {'query': query, 'page': page, 'limit': limit}
```

### File Uploads

```python
@app.post('api/upload')
def upload_file(req):
    file = req.files.get('file')
    if not file:
        return Response().status_code(400).json({'error': 'No file provided'})
    
    # Save file
    import os
    upload_dir = 'uploads'
    os.makedirs(upload_dir, exist_ok=True)
    
    filepath = os.path.join(upload_dir, file.name)
    with open(filepath, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    
    return {
        'filename': file.name,
        'size': file.size,
        'content_type': file.content_type,
        'path': filepath
    }

# Multiple files
@app.post('api/upload-multiple')
def upload_multiple(req):
    files = req.files.getlist('files')
    uploaded = []
    
    for file in files:
        # Save each file
        filepath = f'uploads/{file.name}'
        with open(filepath, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        uploaded.append({'name': file.name, 'size': file.size})
    
    return {'uploaded': uploaded, 'count': len(uploaded)}
```

### Pagination Helper

```python
from shanks import App, Response

def paginate(queryset, page, limit):
    total = queryset.count()
    start = (page - 1) * limit
    end = start + limit
    items = queryset[start:end]
    
    return {
        'items': items,
        'total': total,
        'page': page,
        'limit': limit,
        'pages': (total + limit - 1) // limit
    }

@app.get('api/posts')
def list_posts(req):
    page = int(req.query.get('page', 1))
    limit = int(req.query.get('limit', 10))
    
    posts = Post.find_many()
    result = paginate(posts, page, limit)
    
    return {
        'posts': [{'id': p.id, 'title': p.title} for p in result['items']],
        'pagination': {
            'total': result['total'],
            'page': result['page'],
            'limit': result['limit'],
            'pages': result['pages']
        }
    }
```

### Error Handling

```python
from shanks import App, Response

app = App()

# Global error handler middleware
def error_handler(req):
    try:
        # Continue to next middleware/route
        return None
    except ValueError as e:
        return Response().status_code(400).json({'error': str(e)})
    except PermissionError:
        return Response().status_code(403).json({'error': 'Forbidden'})
    except Exception as e:
        return Response().status_code(500).json({'error': 'Internal server error'})

app.use(error_handler)

# Route-specific error handling
@app.get('api/data/<int:id>')
def get_data(req, id):
    try:
        data = Data.find_unique(id=id)
        if not data:
            return Response().status_code(404).json({'error': 'Not found'})
        return {'data': data}
    except ValueError:
        return Response().status_code(400).json({'error': 'Invalid ID'})
    except Exception as e:
        return Response().status_code(500).json({'error': str(e)})
```

## 🚀 Full Stack Example (React + Shanks)

### Backend (Shanks)

```python
from shanks import App, CORS, SwaggerUI, Model, CharField, TextField, ForeignKey, CASCADE, User
from shanks import authenticate, Response

# Models
class Post(Model):
    title = CharField(max_length=200)
    content = TextField()
    author = ForeignKey(User, on_delete=CASCADE, related_name='posts')

# App
app = App()

# Enable CORS for React
CORS.enable(app,
    origins=['http://localhost:3000'],
    credentials=True
)

# Enable Swagger
SwaggerUI.enable(app, title='Blog API', version='1.0.0')

# Auth
@app.post('api/auth/login')
def login(req):
    user = authenticate(
        username=req.body.get('username'),
        password=req.body.get('password')
    )
    if not user:
        return Response().status_code(401).json({'error': 'Invalid credentials'})
    
    # Create session or JWT token here
    return {'user': {'id': user.id, 'username': user.username}}

# Posts
@app.get('api/posts')
def list_posts(req):
    posts = Post.find_many()
    return {
        'posts': [{
            'id': p.id,
            'title': p.title,
            'content': p.content,
            'author': p.author.username
        } for p in posts]
    }

@app.post('api/posts')
def create_post(req):
    if not req.user.is_authenticated:
        return Response().status_code(401).json({'error': 'Unauthorized'})
    
    post = Post.create(
        title=req.body.get('title'),
        content=req.body.get('content'),
        author=req.user
    )
    return Response().status_code(201).json({'id': post.id})

urlpatterns = app.get_urls()
```

### Frontend (React)

```javascript
// api.js
const API_URL = 'http://localhost:8000/api';

export async function login(username, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ username, password })
  });
  return response.json();
}

export async function getPosts() {
  const response = await fetch(`${API_URL}/posts`, {
    credentials: 'include'
  });
  return response.json();
}

export async function createPost(title, content) {
  const response = await fetch(`${API_URL}/posts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ title, content })
  });
  return response.json();
}

// App.jsx
import { useState, useEffect } from 'react';
import { getPosts, createPost } from './api';

function App() {
  const [posts, setPosts] = useState([]);
  
  useEffect(() => {
    getPosts().then(data => setPosts(data.posts));
  }, []);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    await createPost(formData.get('title'), formData.get('content'));
    const data = await getPosts();
    setPosts(data.posts);
  };
  
  return (
    <div>
      <h1>Blog Posts</h1>
      <form onSubmit={handleSubmit}>
        <input name="title" placeholder="Title" required />
        <textarea name="content" placeholder="Content" required />
        <button type="submit">Create Post</button>
      </form>
      <ul>
        {posts.map(post => (
          <li key={post.id}>
            <h2>{post.title}</h2>
            <p>{post.content}</p>
            <small>by {post.author}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## 🎨 VSCode Extension

Install the Shanks Django extension for VSCode to boost productivity!

### Installation

1. Open VSCode
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Shanks Django"
4. Click Install

Or install from: https://marketplace.visualstudio.com/items?itemName=Ararya.shanks-django

### Available Snippets

| Prefix | Description |
|--------|-------------|
| `shanks-app` | Create new Shanks app |
| `shanks-get` | GET route |
| `shanks-post` | POST route |
| `shanks-put` | PUT route |
| `shanks-delete` | DELETE route |
| `shanks-middleware` | Middleware function |
| `shanks-auth` | Auth middleware |
| `shanks-cors` | Enable CORS |
| `shanks-swagger` | Enable Swagger |
| `shanks-doc` | Swagger documentation |
| `shanks-response` | Response object |
| `shanks-cookie` | Response with cookie |
| `shanks-redirect` | Redirect response |
| `shanks-model` | Create model |
| `shanks-find-many` | Find many records |
| `shanks-find-first` | Find first record |
| `shanks-find-unique` | Find unique record |
| `shanks-create` | Create record |
| `shanks-update` | Update records |
| `shanks-delete-many` | Delete records |
| `shanks-count` | Count records |
| `shanks-update-self` | Update instance |
| `shanks-delete-self` | Delete instance |
| `shanks-user-create` | Create user |
| `shanks-authenticate` | Authenticate user |
| `shanks-mongodb` | MongoDB setup |
| `shanks-redis` | Redis setup |
| `shanks-postgres` | PostgreSQL setup |
| `shanks-full` | Full API template |

### Usage

Type the snippet prefix and press `Tab` to expand!

Example:
```python
# Type: shanks-get [Tab]
@app.get('api/endpoint')
def handler(req):
    return {'data': 'value'}
```

## 📁 Project Structure

### Recommended Structure

```
myproject/
├── manage.py
├── requirements.txt
├── .env
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── posts.py
│   │   └── comments.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── logger.py
│   ├── dto/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   └── utils/
│       ├── __init__.py
│       ├── jwt.py
│       └── validators.py
├── templates/
│   └── index.html
└── static/
    ├── css/
    └── js/
```

### Example: Clean Architecture

```python
# app/models/post.py
from shanks import Model, CharField, TextField, ForeignKey, CASCADE, User

class Post(Model):
    title = CharField(max_length=200)
    content = TextField()
    author = ForeignKey(User, on_delete=CASCADE)

# app/dto/post.py
class PostDTO:
    def __init__(self, data):
        self.title = data.get('title')
        self.content = data.get('content')
    
    def validate(self):
        errors = []
        if not self.title:
            errors.append('Title is required')
        if not self.content:
            errors.append('Content is required')
        return errors

# app/middleware/auth.py
from shanks import Response

def auth_required(req):
    if not req.user.is_authenticated:
        return Response().status_code(401).json({'error': 'Unauthorized'})

# app/routes/posts.py
from shanks import App, Response
from app.models import Post
from app.dto import PostDTO
from app.middleware import auth_required

router = App()

@router.get('api/posts')
def list_posts(req):
    posts = Post.find_many()
    return {'posts': [{'id': p.id, 'title': p.title} for p in posts]}

@router.post('api/posts')
def create_post(req):
    auth_response = auth_required(req)
    if auth_response:
        return auth_response
    
    dto = PostDTO(req.body)
    errors = dto.validate()
    if errors:
        return Response().status_code(400).json({'errors': errors})
    
    post = Post.create(title=dto.title, content=dto.content, author=req.user)
    return Response().status_code(201).json({'id': post.id})

# myproject/urls.py
from django.urls import path, include
from app.routes import posts

urlpatterns = [
    path('', include(posts.router.get_urls())),
]
```

## 🔧 Utility Functions

Shanks wraps common Django utilities for convenience:

```python
from shanks import slugify

# Convert text to URL-friendly slug
slug = slugify('Hello World!')  # 'hello-world'
slug = slugify('Café & Restaurant')  # 'cafe-restaurant'
slug = slugify('Python 3.11 Release')  # 'python-311-release'

# Unicode support
slug = slugify('こんにちは', allow_unicode=True)  # 'こんにちは'
```

## 🧪 Testing

```python
# tests/test_api.py
from django.test import TestCase, Client
from shanks import User
from app.models import Post

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.create(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_list_posts(self):
        # Create test data
        Post.create(title='Test Post', content='Content', author=self.user)
        
        # Test API
        response = self.client.get('/api/posts')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['posts']), 1)
        self.assertEqual(data['posts'][0]['title'], 'Test Post')
    
    def test_create_post(self):
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # Create post
        response = self.client.post('/api/posts', {
            'title': 'New Post',
            'content': 'New Content'
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Post.find_unique(title='New Post'))

# Run tests
# python manage.py test
# or
# shanks test
```

## 🚀 Deployment

### Production Settings

```python
# settings.py
import os
from shanks import DatabaseConfig

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database
DATABASES = {
    'default': DatabaseConfig.from_url(os.getenv('DATABASE_URL'))
}

# Security
SECRET_KEY = os.getenv('SECRET_KEY')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
```

### Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Heroku

```bash
# Install Heroku CLI
# heroku login

# Create app
heroku create myapp

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

### Railway

```bash
# Install Railway CLI
# railway login

# Initialize project
railway init

# Add PostgreSQL
railway add

# Deploy
railway up
```

## 📚 API Reference

### App Class

```python
from shanks import App

app = App()

# HTTP Methods
app.get(path)       # GET route
app.post(path)      # POST route
app.put(path)       # PUT route
app.delete(path)    # DELETE route
app.patch(path)     # PATCH route

# Middleware
app.use(middleware_function)

# Get Django URL patterns
app.get_urls()
```

### Request Object

```python
req.body            # JSON or form data (dict)
req.query           # Query parameters (dict)
req.headers         # HTTP headers (dict)
req.cookies         # Cookies (dict)
req.files           # Uploaded files (dict)
req.user            # Django user object
req.session         # Django session
req.method          # HTTP method (GET, POST, etc.)
req.path            # Request path
req.django          # Original Django request
```

### Response Object

```python
from shanks import Response

Response()
  .json(data)                    # JSON response
  .status_code(code)             # Set status code
  .header(key, value)            # Set header
  .cookie(key, value, **options) # Set cookie
  .redirect(url)                 # Redirect
  .render(request, template, context)  # Render template
  .file(filepath, filename)      # File download
```

### Model Class (Prisma-like ORM)

```python
from shanks import Model

# Query methods
Model.find_many(**filters)      # Find multiple records
Model.find_first(**filters)     # Find first record
Model.find_unique(**filters)    # Find unique record (returns None if not found)
Model.create(**data)            # Create record
Model.update(where, data)       # Update records
Model.delete_many(**filters)    # Delete records
Model.count(**filters)          # Count records

# Instance methods
instance.update_self(**data)    # Update instance
instance.delete_self()          # Delete instance
```

### User Model

```python
from shanks import User, authenticate

# Query methods
User.find_many(**filters)
User.find_first(**filters)
User.find_unique(**filters)
User.create(username, email, password, **kwargs)
User.count(**filters)

# Authentication
authenticate(username, password)  # Returns User or None
```

### Database Helpers

```python
from shanks import DatabaseConfig, MongoDB, Redis

# PostgreSQL/MySQL/SQLite
DatabaseConfig.postgres(host, database, user, password, port=5432)
DatabaseConfig.mysql(host, database, user, password, port=3306)
DatabaseConfig.sqlite(path)
DatabaseConfig.from_url(url)

# MongoDB
MongoDB.connect(host, database, username, password, port=27017)
MongoDB.db  # Access database

# Redis
Redis.connect(host, password, port=6379, db=0)
Redis.client  # Access client
```

### CORS

```python
from shanks import CORS

CORS.enable(app,
    origins=['*'],              # Allowed origins
    methods=['GET', 'POST'],    # Allowed methods
    headers=['Content-Type'],   # Allowed headers
    credentials=False,          # Allow credentials
    max_age=3600               # Preflight cache time
)
```

### Swagger/OpenAPI

```python
from shanks import SwaggerUI

SwaggerUI.enable(app,
    title='API Title',
    version='1.0.0',
    description='API Description'
)

@SwaggerUI.doc(
    summary='Endpoint summary',
    description='Detailed description',
    tags=['Tag'],
    parameters=[...],
    request_body={...},
    responses={...}
)
```

### Utilities

```python
from shanks import slugify

slugify(text, allow_unicode=False)  # Convert to URL-friendly slug
```

## 🤝 Contributing

Contributions are welcome! Please check out the [Contributing Guide](CONTRIBUTING.md).

### Development Setup

```bash
# Clone repository
git clone https://github.com/Ararya/shanks-django.git
cd shanks-django

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .

# Lint
flake8
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- **GitHub**: https://github.com/Ararya/shanks-django
- **PyPI**: https://pypi.org/project/shanks-django/
- **Issues**: https://github.com/Ararya/shanks-django/issues
- **VSCode Extension**: https://marketplace.visualstudio.com/items?itemName=Ararya.shanks-django
- **Documentation**: https://github.com/Ararya/shanks-django/wiki
- **Example Project**: [example-project/](example-project/)

## 💬 Community

- **Discord**: [Join our Discord](https://discord.gg/shanks-django)
- **Twitter**: [@ShanksFramework](https://twitter.com/ShanksFramework)
- **Email**: araryaarch@gmail.com

## ⭐ Show Your Support

If you like Shanks Django, please give it a star on GitHub! ⭐

## 📊 Comparison

| Feature | Django | Express.js | Shanks Django |
|---------|--------|------------|---------------|
| Syntax | Django | Express.js | Express.js |
| ORM | Django ORM | None | Prisma-like |
| Routing | URL patterns | Decorators | Decorators |
| Middleware | Django middleware | Functions | Functions |
| Auto-reload | ✅ | ✅ (nodemon) | ✅ |
| CORS | django-cors-headers | cors | Built-in |
| Swagger | drf-spectacular | swagger-ui | Built-in |
| Database | PostgreSQL, MySQL, SQLite | Any | All + MongoDB, Redis |
| Learning Curve | Steep | Easy | Easy |

## 🎓 Learn More

- [Django Documentation](https://docs.djangoproject.com/)
- [Express.js Documentation](https://expressjs.com/)
- [Prisma Documentation](https://www.prisma.io/docs)
- [Shanks Example Project](example-project/)

## 🙏 Acknowledgments

- Built on top of [Django](https://www.djangoproject.com/)
- Inspired by [Express.js](https://expressjs.com/)
- ORM inspired by [Prisma](https://www.prisma.io/)

---

Made with ❤️ by [Ararya](https://github.com/Ararya)
