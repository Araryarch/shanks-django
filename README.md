# Shanks Django

Framework Python yang menyederhanakan Django dengan syntax mirip Express.js.

## Installation

```bash
pip install shanks-django
```

## Quick Start

1. Install Shanks Django dan Django:
```bash
pip install shanks-django django
```

2. Buat Django project:
```bash
django-admin startproject myproject
cd myproject
```

3. Buat file `api.py`:
```python
from shanks import Ace

app = Ace()

@app.get('api/hello')
def hello(req):
    return {'message': 'Hello World!'}

urlpatterns = app.get_urls()
```

4. Tambahkan ke `urls.py`:
```python
from django.urls import path, include
from . import api

urlpatterns = [
    path('', include(api.urlpatterns)),
]
```

5. Jalankan server:
```bash
python manage.py runserver
```

6. Test API:
```bash
curl http://localhost:8000/api/hello
```

## Features

- ✨ Syntax mirip Express.js
- 🚀 Built on top of Django
- 🔧 Middleware support
- 📦 Request/Response wrapper yang simple

## Example

```python
from shanks import Ace, Request, Response

app = Ace()

# Middleware
def auth_middleware(req: Request):
    if not req.headers.get('Authorization'):
        return Response().status_code(401).json({'error': 'Unauthorized'})

app.use(auth_middleware)

# GET route
@app.get('api/users')
def get_users(req: Request):
    return {'users': []}

# POST route
@app.post('api/users')
def create_user(req: Request):
    data = req.body
    return Response().status_code(201).json(data)

# URL parameters
@app.get('api/users/<int:user_id>')
def get_user(req: Request, user_id):
    return {'id': user_id}

urlpatterns = app.get_urls()
```

## Akses Fitur Django

Shanks Django tetap bisa pakai semua fitur Django:

```python
# Django ORM
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)

@app.get('api/users')
def get_users(req: Request):
    users = User.objects.all()
    return {'users': list(users.values())}

# Django Authentication
@app.get('api/profile')
def profile(req: Request):
    user = req.user  # Django user object
    return {'username': user.username}

# Django Session
@app.get('api/session')
def session(req: Request):
    req.session['key'] = 'value'
    return {'session': req.session.get('key')}

# Django Template
@app.get('dashboard')
def dashboard(req: Request):
    return Response().render(req.django, 'dashboard.html', {'data': 'value'})

# File Upload
@app.post('api/upload')
def upload(req: Request):
    file = req.files.get('file')
    return {'filename': file.name}

# Cookies
@app.post('api/login')
def login(req: Request):
    return Response().json({'ok': True}).cookie('token', 'abc', max_age=3600)

# Redirect
@app.get('old')
def old(req: Request):
    return Response().redirect('/new')

# Full Django Request Access
@app.get('api/advanced')
def advanced(req: Request):
    django_req = req.django  # Full Django request object
    return {'ip': django_req.META.get('REMOTE_ADDR')}
```
