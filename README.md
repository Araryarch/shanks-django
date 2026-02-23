# Shanks Django

Express.js-like framework built on Django. Write Django APIs with Express.js syntax.

## Installation

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

## Quick Start

1. Install Shanks Django and Django:
```bash
pip install shanks-django django
```

2. Create a new project:
```bash
shanks new myproject
cd myproject
```

3. Run the development server:
```bash
shanks run
```

4. Visit http://127.0.0.1:8000/api/hello

Or manually create project:

1. Create Django project:
```bash
django-admin startproject myproject
cd myproject
```

2. Create `api.py`:
```python
from shanks import App

app = App()

@app.get('api/hello')
def hello(req):
    return {'message': 'Hello World!'}

urlpatterns = app.get_urls()
```

3. Add to `urls.py`:
```python
from django.urls import path, include
from . import api

urlpatterns = [
    path('', include(api.urlpatterns)),
]
```

4. Run server:
```bash
shanks run
# or
python manage.py runserver
```

5. Test API:
```bash
curl http://localhost:8000/api/hello
```

## Features

- ✨ Express.js-like syntax
- 🚀 Built on Django
- 🔧 Middleware support
- 📦 Simple Request/Response API
- 🎨 Built-in code formatter
- 🔍 Built-in linter
- � Auto-reload development server (like nodemon)
- �🗄️ Built-in database helpers (PostgreSQL, MySQL, MongoDB, Redis)

## CLI Commands

Shanks comes with built-in CLI tools:

```bash
# Run development server with auto-reload (like nodemon)
shanks run                    # Start on 127.0.0.1:8000
shanks run 3000               # Start on 127.0.0.1:3000
shanks run 0.0.0.0:8000       # Start on all interfaces

# Create new project
shanks new myproject

# Format code with black
shanks format

# Lint code with flake8
shanks lint

# Format and lint
shanks check

# Show help
shanks help
```

## Basic Usage

### Simple Routes

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

urlpatterns = app.get_urls()
```

### Request Object

```python
@app.post('api/data')
def handle_data(req):
    # Get request body (JSON or form data)
    data = req.body
    
    # Get query parameters
    page = req.query.get('page', 1)
    
    # Get headers
    auth = req.headers.get('Authorization')
    
    # Get cookies
    token = req.cookies.get('token')
    
    # Get uploaded files
    file = req.files.get('file')
    
    # Get authenticated user (Django)
    user = req.user
    
    # Get session (Django)
    req.session['key'] = 'value'
    
    # Access full Django request
    django_req = req.django
    
    return {'status': 'ok'}
```

### Response Object

```python
from shanks import App, Response

app = App()

# JSON response
@app.get('api/data')
def get_data(req):
    return Response().json({'data': 'value'})

# Custom status code
@app.post('api/create')
def create(req):
    return Response().status_code(201).json({'created': True})

# Set headers
@app.get('api/custom')
def custom(req):
    return Response().header('X-Custom', 'value').json({'ok': True})

# Set cookies
@app.post('api/login')
def login(req):
    return Response().cookie('token', 'abc123', max_age=3600).json({'logged_in': True})

# Redirect
@app.get('old-url')
def old_url(req):
    return Response().redirect('/new-url')

# Render Django template
@app.get('dashboard')
def dashboard(req):
    return Response().render(req.django, 'dashboard.html', {'title': 'Dashboard'})
```

### Middleware

```python
from shanks import App, Response

app = App()

# Simple middleware
def logger(req):
    print(f"{req.method} {req.path}")

app.use(logger)

# Auth middleware
def auth_middleware(req):
    if not req.headers.get('Authorization'):
        return Response().status_code(401).json({'error': 'Unauthorized'})

app.use(auth_middleware)

@app.get('api/protected')
def protected(req):
    return {'data': 'secret'}
```

## Django Integration

Shanks is built on Django, so you can use all Django features:

### Django ORM

```python
from django.db import models
from shanks import App

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

app = App()

@app.get('api/users')
def get_users(req):
    users = User.objects.all()
    return {'users': list(users.values())}

@app.post('api/users')
def create_user(req):
    user = User.objects.create(
        name=req.body.get('name'),
        email=req.body.get('email')
    )
    return Response().status_code(201).json({'id': user.id})
```

### Django Authentication

```python
from django.contrib.auth import authenticate, login
from shanks import App, Response

app = App()

@app.post('api/login')
def user_login(req):
    username = req.body.get('username')
    password = req.body.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        login(req.django, user)
        return {'success': True}
    
    return Response().status_code(401).json({'error': 'Invalid credentials'})

@app.get('api/profile')
def profile(req):
    if not req.user.is_authenticated:
        return Response().status_code(401).json({'error': 'Not authenticated'})
    
    return {
        'username': req.user.username,
        'email': req.user.email
    }
```

### Django Sessions

```python
@app.get('api/cart')
def get_cart(req):
    cart = req.session.get('cart', [])
    return {'cart': cart}

@app.post('api/cart')
def add_to_cart(req):
    cart = req.session.get('cart', [])
    cart.append(req.body.get('item'))
    req.session['cart'] = cart
    return {'cart': cart}
```

### File Uploads

```python
@app.post('api/upload')
def upload_file(req):
    file = req.files.get('file')
    if not file:
        return Response().status_code(400).json({'error': 'No file'})
    
    # Save file
    with open(f'uploads/{file.name}', 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    
    return {'filename': file.name, 'size': file.size}
```

### Django Templates

```python
@app.get('dashboard')
def dashboard(req):
    context = {
        'user': req.user,
        'data': {'title': 'Dashboard', 'count': 42}
    }
    return Response().render(req.django, 'dashboard.html', context)
```

## Database Support

Shanks provides built-in helpers for multiple databases.

### PostgreSQL

```python
# settings.py
from shanks import DatabaseConfig

DATABASES = {
    'default': DatabaseConfig.postgres(
        host='localhost',
        database='mydb',
        user='myuser',
        password='mypass'
    )
}

# Or from environment variable
import os
DATABASES = {
    'default': DatabaseConfig.from_url(os.getenv('DATABASE_URL'))
}
```

### MySQL

```python
# settings.py
from shanks import DatabaseConfig

DATABASES = {
    'default': DatabaseConfig.mysql(
        host='localhost',
        database='mydb',
        user='root',
        password='mypass'
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
# app.py or startup
from shanks import MongoDB, App

# Connect to MongoDB
MongoDB.connect(
    host='localhost',
    database='mydb',
    username='user',
    password='pass'
)

app = App()

@app.get('api/users')
def get_users(req):
    users = list(MongoDB.db.users.find({}, {'_id': 0}))
    return {'users': users}

@app.post('api/users')
def create_user(req):
    user_data = {
        'name': req.body.get('name'),
        'email': req.body.get('email')
    }
    result = MongoDB.db.users.insert_one(user_data)
    return {'id': str(result.inserted_id)}
```

### Redis

```python
# app.py or startup
from shanks import Redis, App

# Connect to Redis
Redis.connect(
    host='localhost',
    password='mypass'
)

app = App()

@app.get('api/cache/<key>')
def get_cache(req, key):
    value = Redis.client.get(key)
    return {'value': value}

@app.post('api/cache')
def set_cache(req):
    key = req.body.get('key')
    value = req.body.get('value')
    ttl = req.body.get('ttl', 3600)
    
    Redis.client.setex(key, ttl, value)
    return {'success': True}
```

### Multiple Databases

```python
from shanks import App, MongoDB, Redis
from django.db import models

# Django ORM Model (PostgreSQL/MySQL/SQLite)
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

app = App()

@app.post('api/register')
def register(req):
    # Save to PostgreSQL
    user = User.objects.create(
        name=req.body.get('name'),
        email=req.body.get('email')
    )
    
    # Cache in Redis
    Redis.client.setex(f'user:{user.id}', 3600, user.email)
    
    # Log in MongoDB
    MongoDB.db.logs.insert_one({
        'user_id': user.id,
        'action': 'register'
    })
    
    return {'id': user.id}
```

## Advanced Usage

### URL Parameters

```python
# Path parameters
@app.get('api/users/<int:user_id>')
def get_user(req, user_id):
    return {'id': user_id}

@app.get('api/posts/<slug:slug>')
def get_post(req, slug):
    return {'slug': slug}

# Multiple parameters
@app.get('api/users/<int:user_id>/posts/<int:post_id>')
def get_user_post(req, user_id, post_id):
    return {'user_id': user_id, 'post_id': post_id}
```

### Error Handling

```python
from shanks import App, Response

app = App()

# Error middleware
def error_handler(req):
    try:
        # Process request
        pass
    except Exception as e:
        return Response().status_code(500).json({'error': str(e)})

app.use(error_handler)

# Custom error responses
@app.get('api/data')
def get_data(req):
    try:
        # Your logic
        return {'data': 'value'}
    except ValueError:
        return Response().status_code(400).json({'error': 'Invalid data'})
    except Exception as e:
        return Response().status_code(500).json({'error': 'Server error'})
```

### CORS Support

```python
from shanks import App, CORS

app = App()

# Enable CORS for all origins
CORS.enable(app)

# Or specific origins
CORS.enable(app,
    origins=['http://localhost:3000', 'https://myapp.com'],
    methods=['GET', 'POST', 'PUT', 'DELETE'],
    headers=['Content-Type', 'Authorization'],
    credentials=True
)

@app.get('api/data')
def get_data(req):
    return {'data': 'value'}
```

### Complete React + Shanks Example

```python
from shanks import App, CORS, Response

app = App()

# Enable CORS for React dev server
CORS.enable(app,
    origins=['http://localhost:3000'],
    credentials=True
)

@app.post('api/login')
def login(req):
    username = req.body.get('username')
    password = req.body.get('password')
    
    if username == 'admin' and password == 'password':
        return Response().cookie('session', 'abc123').json({
            'success': True
        })
    
    return Response().status_code(401).json({'error': 'Invalid'})

@app.get('api/protected')
def protected(req):
    # Cookies automatically sent from frontend
    return {'data': 'secret'}
```

Frontend (React):
```javascript
// Login with credentials
fetch('http://localhost:8000/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include', // Important for cookies
  body: JSON.stringify({ username: 'admin', password: 'password' })
})

// Access protected route
fetch('http://localhost:8000/api/protected', {
  credentials: 'include' // Sends cookies
})
```

## Project Structure

```
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── api.py          # Your Shanks routes
├── templates/
│   └── dashboard.html
└── requirements.txt
```

## Complete Example

```python
from shanks import App, Request, Response
from django.db import models
from django.contrib.auth import authenticate, login

# Models
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# App
app = App()

# Middleware
def logger(req):
    print(f"{req.method} {req.path}")

def auth_check(req):
    if req.path.startswith('api/protected') and not req.user.is_authenticated:
        return Response().status_code(401).json({'error': 'Unauthorized'})

app.use(logger)
app.use(auth_check)

# Routes
@app.get('api/posts')
def get_posts(req):
    posts = Post.objects.all().order_by('-created_at')
    return {'posts': list(posts.values())}

@app.get('api/posts/<int:post_id>')
def get_post(req, post_id):
    try:
        post = Post.objects.get(id=post_id)
        return {
            'id': post.id,
            'title': post.title,
            'content': post.content
        }
    except Post.DoesNotExist:
        return Response().status_code(404).json({'error': 'Not found'})

@app.post('api/posts')
def create_post(req):
    post = Post.objects.create(
        title=req.body.get('title'),
        content=req.body.get('content')
    )
    return Response().status_code(201).json({'id': post.id})

@app.put('api/posts/<int:post_id>')
def update_post(req, post_id):
    try:
        post = Post.objects.get(id=post_id)
        post.title = req.body.get('title', post.title)
        post.content = req.body.get('content', post.content)
        post.save()
        return {'updated': True}
    except Post.DoesNotExist:
        return Response().status_code(404).json({'error': 'Not found'})

@app.delete('api/posts/<int:post_id>')
def delete_post(req, post_id):
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return {'deleted': True}
    except Post.DoesNotExist:
        return Response().status_code(404).json({'error': 'Not found'})

@app.post('api/login')
def user_login(req):
    user = authenticate(
        username=req.body.get('username'),
        password=req.body.get('password')
    )
    if user:
        login(req.django, user)
        return {'success': True}
    return Response().status_code(401).json({'error': 'Invalid credentials'})

@app.get('api/protected/data')
def protected_data(req):
    return {'secret': 'data', 'user': req.user.username}

urlpatterns = app.get_urls()
```

## Contributing

Contributions are welcome! Please check out the [Contributing Guide](CONTRIBUTING.md).

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Links

- GitHub: https://github.com/Ararya/shanks-django
- PyPI: https://pypi.org/project/shanks-django/
- Issues: https://github.com/Ararya/shanks-django/issues
